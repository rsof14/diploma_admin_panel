CREATE TABLE IF NOT EXISTS public.asset
(
    "ISIN" character(12) COLLATE pg_catalog."default" NOT NULL,
    ticker character(10) COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    sector text COLLATE pg_catalog."default",
    CONSTRAINT asset_pkey PRIMARY KEY ("ISIN")
);

CREATE TABLE IF NOT EXISTS public.currency
(
    currency character(3) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    CONSTRAINT currency_pkey PRIMARY KEY (currency)
);

CREATE TABLE IF NOT EXISTS public.customer
(
    id uuid NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    branch text COLLATE pg_catalog."default",
    CONSTRAINT customer_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.objects_permissions
(
    object text COLLATE pg_catalog."default" NOT NULL,
    role_id uuid NOT NULL,
    permission text COLLATE pg_catalog."default" NOT NULL,
    strategy_type text COLLATE pg_catalog."default",
    id uuid,
    CONSTRAINT objects_permissions_pkey PRIMARY KEY (object, role_id)
);

CREATE TABLE IF NOT EXISTS public.permissions
(
    permission text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT permissions_pkey PRIMARY KEY (permission)
);

CREATE TABLE IF NOT EXISTS public.portfolio
(
    account character(8) COLLATE pg_catalog."default" NOT NULL,
    customer_id uuid NOT NULL,
    strategy_id uuid,
    structure json,
    asset_manager uuid,
    creation_date date NOT NULL,
    updated boolean,
    CONSTRAINT portfolio_pkey PRIMARY KEY (account)
);

CREATE TABLE IF NOT EXISTS public.portfolio_risks
(
    risk_metric text COLLATE pg_catalog."default" NOT NULL,
    account character(8) COLLATE pg_catalog."default" NOT NULL,
    value real NOT NULL,
    updated boolean,
    violation boolean,
    CONSTRAINT portfolio_risks_pkey PRIMARY KEY (risk_metric, account)
);

CREATE TABLE IF NOT EXISTS public.portfolio_strategy_history
(
    account character(8) COLLATE pg_catalog."default" NOT NULL,
    changed_date date NOT NULL,
    strategy_id uuid NOT NULL,
    CONSTRAINT portfolio_strategy_history_pkey PRIMARY KEY (changed_date, account)
);

CREATE TABLE IF NOT EXISTS public.portfolio_values
(
    account character(8) COLLATE pg_catalog."default" NOT NULL,
    date_ date NOT NULL,
    value real NOT NULL,
    CONSTRAINT portfolio_values_pkey PRIMARY KEY (account, date_)
);

CREATE TABLE IF NOT EXISTS public.risk_metrics
(
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT risk_metrics_pkey PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS public.risk_profile
(
    name text COLLATE pg_catalog."default" NOT NULL,
    max_var real NOT NULL,
    CONSTRAINT risk_profile_pkey PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS public.roles
(
    id uuid NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT roles_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.strategy
(
    id uuid NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    currency character(3) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    type text COLLATE pg_catalog."default" NOT NULL,
    risk_profile text COLLATE pg_catalog."default" NOT NULL,
    structure json NOT NULL,
    valid boolean,
    management_fee real,
    success_fee real,
    benchmark json,
    CONSTRAINT strategy_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.strategy_type
(
    type text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT strategy_type_pkey PRIMARY KEY (type)
);

CREATE TABLE IF NOT EXISTS public.support_messages
(
    msg_date date NOT NULL,
    user_id uuid NOT NULL,
    message text COLLATE pg_catalog."default" NOT NULL,
    answer text COLLATE pg_catalog."default",
    done boolean,
    CONSTRAINT support_messages_pkey PRIMARY KEY (msg_date, user_id)
);

CREATE TABLE IF NOT EXISTS public.system_objects
(
    object_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT system_objects_pkey PRIMARY KEY (object_name)
);

CREATE TABLE IF NOT EXISTS public."user"
(
    id uuid NOT NULL,
    login text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    created_at date NOT NULL,
    is_superuser boolean,
    role_id uuid,
    CONSTRAINT user_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.login_history
(
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    user_agent character(255) COLLATE pg_catalog."default" NOT NULL,
    auth_datetime timestamp without time zone NOT NULL,
    CONSTRAINT login_history_pkey PRIMARY KEY (id),
    CONSTRAINT login_history_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

ALTER TABLE IF EXISTS public.objects_permissions
    ADD CONSTRAINT objects_permissions_object_fkey FOREIGN KEY (object)
    REFERENCES public.system_objects (object_name) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.objects_permissions
    ADD CONSTRAINT objects_permissions_permission_fkey FOREIGN KEY (permission)
    REFERENCES public.permissions (permission) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.objects_permissions
    ADD CONSTRAINT objects_permissions_role_id_fkey FOREIGN KEY (role_id)
    REFERENCES public.roles (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.objects_permissions
    ADD CONSTRAINT objects_permissions_strategy_type_fkey FOREIGN KEY (strategy_type)
    REFERENCES public.strategy_type (type) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio
    ADD CONSTRAINT portfolio_asset_manager_fkey FOREIGN KEY (asset_manager)
    REFERENCES public."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio
    ADD CONSTRAINT portfolio_customer_id_fkey FOREIGN KEY (customer_id)
    REFERENCES public.customer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio
    ADD CONSTRAINT portfolio_strategy_id_fkey FOREIGN KEY (strategy_id)
    REFERENCES public.strategy (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio_risks
    ADD CONSTRAINT portfolio_risks_account_fkey FOREIGN KEY (account)
    REFERENCES public.portfolio (account) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio_risks
    ADD CONSTRAINT portfolio_risks_risk_metric_fkey FOREIGN KEY (risk_metric)
    REFERENCES public.risk_metrics (name) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio_strategy_history
    ADD CONSTRAINT portfolio_strategy_history_account_fkey FOREIGN KEY (account)
    REFERENCES public.portfolio (account) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio_strategy_history
    ADD CONSTRAINT portfolio_strategy_history_strategy_id_fkey FOREIGN KEY (strategy_id)
    REFERENCES public.strategy (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.portfolio_values
    ADD CONSTRAINT portfolio_values_account_fkey FOREIGN KEY (account)
    REFERENCES public.portfolio (account) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS public.strategy
    ADD CONSTRAINT strategy_currency_fkey FOREIGN KEY (currency)
    REFERENCES public.currency (currency) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS public.strategy
    ADD CONSTRAINT strategy_risk_profile_fkey FOREIGN KEY (risk_profile)
    REFERENCES public.risk_profile (name) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS public.strategy
    ADD CONSTRAINT strategy_type_fkey FOREIGN KEY (type)
    REFERENCES public.strategy_type (type) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS public.support_messages
    ADD CONSTRAINT support_messages_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS public."user"
    ADD CONSTRAINT user_role_id_fkey FOREIGN KEY (role_id)
    REFERENCES public.roles (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL
    NOT VALID;