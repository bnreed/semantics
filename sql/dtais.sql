-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    id bigint NOT NULL DEFAULT nextval('documents_id_seq'::regclass),
    question1 text COLLATE pg_catalog."default" NOT NULL,
    embedding1 vector(1536) NOT NULL,
    experiment_id bigint,
    question2 text COLLATE pg_catalog."default" NOT NULL,
    embedding2 vector NOT NULL,
    qid1 bigint,
    qid2 bigint,
    model_response1 text COLLATE pg_catalog."default",
    model_response2 text COLLATE pg_catalog."default",
    model_embedding1 vector,
    model_embedding2 vector,
    is_duplicate integer,
    model_embedding_cos double precision,
    question_embedding_cos double precision,
    CONSTRAINT documents_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to bnreed;
-- Index: documents_embedding_idx

-- DROP INDEX IF EXISTS public.documents_embedding_idx;

CREATE INDEX IF NOT EXISTS documents_embedding_idx
    ON public.documents USING ivfflat
    (embedding1 vector_cosine_ops)
    TABLESPACE pg_default;