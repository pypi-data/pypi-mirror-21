# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import CommandError
from django.db import connection, transaction

from psycopg2.extensions import quote_ident


class DatabaseRole(object):
    ROLE_NAME = 'rolname'

    def __init__(self, rolename, create=False, commit=True,
                 db_connection=None, db_transaction=None):
        self.rolename = rolename
        self.connection = (connection if db_connection is None
                                      else db_connection)
        self.transaction = (transaction if db_transaction is None
                                        else db_transaction)
        exists = self.exists(rolename)

        if create:
            if exists:
                raise CommandError("Role already exists: %s" % rolename)

            cursor = self.connection.cursor()
            role = quote_ident(rolename, cursor.cursor)
            cursor.execute('CREATE ROLE %s' % role)
            if commit and not self.exists(rolename):
                raise CommandError("Role couldn't be created: %s" % rolename)
        elif not exists:
            raise CommandError("Role doesn't exist: %s" % rolename)

    def delete(self, commit=True):
        cursor = self.connection.cursor()
        role = quote_ident(self.rolename, cursor.cursor)
        cursor.execute('DROP ROLE %s' % role)
        if commit and self.exists(self.rolename):
            raise CommandError("Role cannot be deleted: %s" % self.rolename)

    @classmethod
    def exists(cls, rolename, db_connection=None):
        db_connection = connection if db_connection is None else db_connection

        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM pg_roles WHERE rolname=%s', (rolename,))
        role = cursor.fetchone()
        return role is not None

    def get_users(self, order_by=ROLE_NAME):
        cursor = self.connection.cursor()
        query = ('SELECT rolname FROM pg_authid '
                 ' WHERE oid IN ('
                 '       SELECT member FROM pg_auth_members '
                 '        WHERE roleid = ('
                 '              SELECT oid FROM pg_authid '
                 '               WHERE rolname=%%s)) '
                 'ORDER BY %s' % order_by)
        cursor.execute(query, (self.rolename,))
        users_result = cursor.fetchall()
        users = [result[0] for result in users_result]
        return users

    def grant(self, user, commit=True):
        cursor = self.connection.cursor()
        role = quote_ident(self.rolename, cursor.cursor)
        username = quote_ident(user.username, cursor.cursor)
        cursor.execute('GRANT %s TO %s' % (role, username))

    def revoke(self, user, commit=True):
        cursor = self.connection.cursor()
        role = quote_ident(self.rolename, cursor.cursor)
        username = quote_ident(user.username, cursor.cursor)
        cursor.execute('REVOKE %s FROM %s' % (role, username))
        if commit and user.has_role(self):
            raise CommandError("Role cannot be revoked: %s" % self.rolename)
