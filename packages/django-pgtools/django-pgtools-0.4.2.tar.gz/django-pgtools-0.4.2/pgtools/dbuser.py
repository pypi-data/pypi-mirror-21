# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import CommandError
from django.db import connection, transaction

from psycopg2.extensions import quote_ident


class DatabaseUser(object):

    def __init__(self, username, password=None, commit=True, create=True,
                 db_connection=None, db_transaction=None):
        self.username = username
        self.connection = (connection if db_connection is None
                                      else db_connection)
        self.transaction = (transaction if db_transaction is None
                                        else db_transaction)
        exists = self.exists(username, db_connection=db_connection)

        if create:
            if exists:
                raise CommandError("User already exists: %s" % username)

            cursor = self.connection.cursor()
            user = quote_ident(username, cursor.cursor)
            if password is None:
                cursor.execute('CREATE USER %s' % user)
            else:
                cursor.execute('CREATE USER %s PASSWORD %%s' % user,
                               (password,))
            if commit and not self.exists(username):
                raise CommandError(
                    "User couldn't be created: %s" % username)
        elif not exists:
            raise CommandError("User doesn't exist: %s" % username)

    def delete(self, commit=True):
        cursor = self.connection.cursor()
        user = quote_ident(self.username, cursor.cursor)
        cursor.execute('DROP USER %s' % user)
        if commit and self.exists(self.username):
            raise CommandError("User cannot be deleted: %s" % self.username)

    @classmethod
    def exists(cls, username, db_connection=None):
        db_connection = connection if db_connection is None else db_connection
        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM pg_roles WHERE rolname=%s', (username,))
        user = cursor.fetchone()
        return user is not None

    def has_role(self, role):
        cursor = self.connection.cursor()
        query = ('SELECT * FROM pg_auth_members '
                 ' WHERE roleid = ('
                 '       SELECT oid FROM pg_authid '
                 '        WHERE rolname=%s) '
                 '   AND member = ('
                 '       SELECT oid FROM pg_authid '
                 '        WHERE rolname=%s)')
        cursor.execute(query, (role.rolename, self.username))
        membership = cursor.fetchone()
        return bool(membership)
