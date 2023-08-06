# -*- coding: utf-8 -*-
# Copyright: Albertix <albertix@live.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sqlite3 as sql

NEW_DB = '''
CREATE TABLE col (
    id              integer primary key,
    crt             integer not null,
    mod             integer not null,
    scm             integer not null,
    ver             integer not null,
    dty             integer not null,
    usn             integer not null,
    ls              integer not null,
    conf            text not null,
    models          text not null,
    decks           text not null,
    dconf           text not null,
    tags            text not null
);
CREATE TABLE notes (
    id              integer primary key,   /* 0 */
    guid            text not null,         /* 1 */
    mid             integer not null,      /* 2 */
    mod             integer not null,      /* 3 */
    usn             integer not null,      /* 4 */
    tags            text not null,         /* 5 */
    flds            text not null,         /* 6 */
    sfld            integer not null,      /* 7 */
    csum            integer not null,      /* 8 */
    flags           integer not null,      /* 9 */
    data            text not null          /* 10 */
);
CREATE TABLE cards (
    id              integer primary key,   /* 0 */
    nid             integer not null,      /* 1 */
    did             integer not null,      /* 2 */
    ord             integer not null,      /* 3 */
    mod             integer not null,      /* 4 */
    usn             integer not null,      /* 5 */
    type            integer not null,      /* 6 */
    queue           integer not null,      /* 7 */
    due             integer not null,      /* 8 */
    ivl             integer not null,      /* 9 */
    factor          integer not null,      /* 10 */
    reps            integer not null,      /* 11 */
    lapses          integer not null,      /* 12 */
    left            integer not null,      /* 13 */
    odue            integer not null,      /* 14 */
    odid            integer not null,      /* 15 */
    flags           integer not null,      /* 16 */
    data            text not null          /* 17 */
);
CREATE TABLE revlog (
    id              integer primary key,
    cid             integer not null,
    usn             integer not null,
    ease            integer not null,
    ivl             integer not null,
    lastIvl         integer not null,
    factor          integer not null,
    time            integer not null,
    type            integer not null
);
CREATE TABLE graves (
    usn             integer not null,
    oid             integer not null,
    type            integer not null
);
CREATE INDEX ix_notes_usn on notes (usn);
CREATE INDEX ix_cards_usn on cards (usn);
CREATE INDEX ix_revlog_usn on revlog (usn);
CREATE INDEX ix_cards_nid on cards (nid);
CREATE INDEX ix_cards_sched on cards (did, queue, due);
CREATE INDEX ix_revlog_cid on revlog (cid);
CREATE INDEX ix_notes_csum on notes (csum);
'''


def create_db(col, notes, cards, db_path):

    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(NEW_DB)
    conn.commit()

    cursor.execute('INSERT INTO col(id,crt,mod,scm,ver,'
                   'dty,usn,ls,conf,models,'
                   'decks,dconf,tags)'
                   ' VALUES (?,?,?,?,?,'
                   '?,?,?,?,?,'
                   '?,?,?)',
                   col)
    cursor.executemany("INSERT INTO notes(id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data)"
                       " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", notes)
    cursor.executemany("INSERT INTO cards"
                       "(id,nid,did,ord,mod,"
                       "usn,type,queue,due,ivl,"
                       "factor,reps,lapses,left,odue,"
                       "odid,flags,data)"
                       " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cards)

    conn.commit()
    conn.close()
