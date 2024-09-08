CREATE TABLE IF NOT EXISTS public."ADDRESS"
(
    member_user_id integer NOT NULL,
    house_number character varying(20) COLLATE pg_catalog."default",
    street character varying(100) COLLATE pg_catalog."default",
    town character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT "ADDRESS_pkey" PRIMARY KEY (member_user_id),
    CONSTRAINT "ADDRESS_member_user_id_fkey" FOREIGN KEY (member_user_id)
        REFERENCES public."MEMBER" (member_user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public."APPOINTMENT"
(
    appointment_id integer NOT NULL DEFAULT nextval('"APPOINTMENT_appointment_id_seq"'::regclass),
    caregiver_user_id integer,
    member_user_id integer,
    appointment_date date,
    appointment_time time without time zone,
    work_hours double precision,
    status character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT "APPOINTMENT_pkey" PRIMARY KEY (appointment_id),
    CONSTRAINT "APPOINTMENT_caregiver_user_id_fkey" FOREIGN KEY (caregiver_user_id)
        REFERENCES public."CAREGIVER" (caregiver_user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "APPOINTMENT_member_user_id_fkey" FOREIGN KEY (member_user_id)
        REFERENCES public."MEMBER" (member_user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public."CAREGIVER"
(
    caregiver_user_id integer NOT NULL DEFAULT nextval('"CAREGIVER_caregiver_user_id_seq"'::regclass),
    photo character varying COLLATE pg_catalog."default",
    gender character varying(10) COLLATE pg_catalog."default",
    caregiving_type character varying(50) COLLATE pg_catalog."default",
    hourly_rate double precision,
    CONSTRAINT "CAREGIVER_pkey" PRIMARY KEY (caregiver_user_id)
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public."JOB"
(
    job_id integer NOT NULL DEFAULT nextval('"JOB_job_id_seq"'::regclass),
    member_user_id integer,
    required_caregiving_type character varying(50) COLLATE pg_catalog."default",
    other_requirements text COLLATE pg_catalog."default",
    date_posted date,
    CONSTRAINT "JOB_pkey" PRIMARY KEY (job_id),
    CONSTRAINT "JOB_member_user_id_fkey" FOREIGN KEY (member_user_id)
        REFERENCES public."MEMBER" (member_user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public."JOB_APPLICATION"
(
    caregiver_user_id integer NOT NULL,
    job_id integer NOT NULL,
    date_applied date,
    CONSTRAINT "JOB_APPLICATION_pkey" PRIMARY KEY (caregiver_user_id, job_id),
    CONSTRAINT "JOB_APPLICATION_caregiver_user_id_fkey" FOREIGN KEY (caregiver_user_id)
        REFERENCES public."CAREGIVER" (caregiver_user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "JOB_APPLICATION_job_id_fkey" FOREIGN KEY (job_id)
        REFERENCES public."JOB" (job_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public."MEMBER"
(
    member_user_id integer NOT NULL DEFAULT nextval('"MEMBER_member_user_id_seq"'::regclass),
    house_rules text COLLATE pg_catalog."default",
    CONSTRAINT "MEMBER_pkey" PRIMARY KEY (member_user_id)
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public."USER"
(
    user_id integer NOT NULL DEFAULT nextval('"USER_user_id_seq"'::regclass),
    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    given_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    surname character varying(50) COLLATE pg_catalog."default" NOT NULL,
    city character varying(100) COLLATE pg_catalog."default",
    phone_number character varying(20) COLLATE pg_catalog."default",
    profile_description text COLLATE pg_catalog."default",
    password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "USER_pkey" PRIMARY KEY (user_id)
)

TABLESPACE pg_default;