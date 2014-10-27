pragma foreign_keys = on;

drop table if exists linkstats;
drop table if exists ngrams;

create table ngrams (
    id integer primary key default NULL,
    ngram text unique not NULL,
    tf integer default 0,
    df integer default 0
);

create table linkstats (
    ngram_id integer not NULL,
    target text not NULL,
    count integer not NULL,
    foreign key(ngram_id) references ngrams(id)
);

create unique index target_anchor on linkstats(ngram_id, target);
