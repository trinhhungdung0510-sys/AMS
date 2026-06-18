--
-- PostgreSQL database dump
--

\restrict TU7cn3IIwq1G8KtTmDWVY3jZV3VWru5vgtYY6CtvUhhmeLlEQg1X3LlUcxy2ajF

-- Dumped from database version 16.14
-- Dumped by pg_dump version 16.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_models; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.ai_models (
    id character varying(20) NOT NULL,
    model_name character varying(120) NOT NULL,
    model_type character varying(80) NOT NULL,
    version character varying(40) NOT NULL,
    enabled boolean NOT NULL
);


ALTER TABLE public.ai_models OWNER TO ams;

--
-- Name: ai_tasks; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.ai_tasks (
    id character varying(24) NOT NULL,
    camera_id character varying(20) NOT NULL,
    category character varying(80) NOT NULL,
    status character varying(20) NOT NULL,
    priority integer NOT NULL,
    result text NOT NULL,
    created_at character varying(32) NOT NULL,
    processed_at character varying(32)
);


ALTER TABLE public.ai_tasks OWNER TO ams;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ams;

--
-- Name: alert_categories; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.alert_categories (
    code character varying(80) NOT NULL,
    label character varying(160) NOT NULL,
    severity character varying(20) NOT NULL
);


ALTER TABLE public.alert_categories OWNER TO ams;

--
-- Name: animal_intrusion_policies; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.animal_intrusion_policies (
    id character varying(24) NOT NULL,
    object_type character varying(40) NOT NULL,
    allowed_zones json NOT NULL,
    restricted_zones json NOT NULL,
    severity character varying(20) NOT NULL,
    enabled boolean NOT NULL
);


ALTER TABLE public.animal_intrusion_policies OWNER TO ams;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.audit_logs (
    id character varying(24) NOT NULL,
    user_id character varying(20) NOT NULL,
    action character varying(80) NOT NULL,
    resource_type character varying(80) NOT NULL,
    resource_id character varying(80) NOT NULL,
    metadata_json text NOT NULL,
    created_at character varying(32) NOT NULL
);


ALTER TABLE public.audit_logs OWNER TO ams;

--
-- Name: biosecurity_rules; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.biosecurity_rules (
    id character varying(24) NOT NULL,
    severity character varying(20) NOT NULL,
    enabled boolean NOT NULL,
    object_type character varying(40),
    from_zone character varying(40),
    to_zone character varying(40),
    required_zone character varying(40),
    rule_code character varying(80) NOT NULL,
    rule_name_vi character varying(160) NOT NULL,
    rule_name_en character varying(160) NOT NULL,
    category character varying(40) NOT NULL,
    description text NOT NULL,
    created_at character varying(32) NOT NULL
);


ALTER TABLE public.biosecurity_rules OWNER TO ams;

--
-- Name: camera_health; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.camera_health (
    id character varying(24) NOT NULL,
    farm_id character varying(20) NOT NULL,
    camera_id character varying(20) NOT NULL,
    fps integer NOT NULL,
    bitrate double precision NOT NULL,
    last_seen character varying(32) NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.camera_health OWNER TO ams;

--
-- Name: camera_streams; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.camera_streams (
    id character varying(20) NOT NULL,
    camera_id character varying(20) NOT NULL,
    rtsp_url character varying(255) NOT NULL,
    fps integer NOT NULL,
    resolution character varying(20) NOT NULL,
    stream_status character varying(20) NOT NULL
);


ALTER TABLE public.camera_streams OWNER TO ams;

--
-- Name: cameras; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.cameras (
    id character varying(20) NOT NULL,
    name character varying(120) NOT NULL,
    zone character varying(80) NOT NULL,
    ip_address character varying(45) NOT NULL,
    status character varying(20) NOT NULL,
    resolution character varying(20) NOT NULL,
    uptime double precision NOT NULL,
    fps integer NOT NULL,
    is_active boolean NOT NULL,
    farm_id character varying(20) NOT NULL
);


ALTER TABLE public.cameras OWNER TO ams;

--
-- Name: edge_devices; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.edge_devices (
    id character varying(24) NOT NULL,
    farm_id character varying(20) NOT NULL,
    device_name character varying(120) NOT NULL,
    device_type character varying(60) NOT NULL,
    serial_number character varying(80) NOT NULL,
    status character varying(20) NOT NULL,
    assigned_cameras integer NOT NULL
);


ALTER TABLE public.edge_devices OWNER TO ams;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.employees (
    id character varying(24) NOT NULL,
    employee_code character varying(40) NOT NULL,
    full_name character varying(120) NOT NULL,
    department character varying(80) NOT NULL,
    assigned_zone character varying(40) NOT NULL,
    uniform_color character varying(40) NOT NULL,
    face_image character varying(255) NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public.employees OWNER TO ams;

--
-- Name: event_snapshots; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.event_snapshots (
    id character varying(20) NOT NULL,
    event_id character varying(20) NOT NULL,
    image_path character varying(255) NOT NULL,
    thumbnail_path character varying(255) NOT NULL
);


ALTER TABLE public.event_snapshots OWNER TO ams;

--
-- Name: events; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.events (
    id character varying(20) NOT NULL,
    camera_id character varying(20) NOT NULL,
    alert_type character varying(80) NOT NULL,
    zone character varying(80) NOT NULL,
    severity character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    handler character varying(120) NOT NULL,
    confidence integer NOT NULL,
    occurred_at character varying(32) NOT NULL,
    category character varying(80) NOT NULL,
    farm_id character varying(20) NOT NULL,
    violation_code character varying(40)
);


ALTER TABLE public.events OWNER TO ams;

--
-- Name: farm_layout_templates; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.farm_layout_templates (
    id character varying(24) NOT NULL,
    name character varying(160) NOT NULL,
    description text NOT NULL,
    version character varying(20) NOT NULL
);


ALTER TABLE public.farm_layout_templates OWNER TO ams;

--
-- Name: farm_map_objects; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.farm_map_objects (
    id character varying(20) NOT NULL,
    object_type character varying(40) NOT NULL,
    name character varying(120) NOT NULL,
    zone character varying(80) NOT NULL,
    x double precision NOT NULL,
    y double precision NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.farm_map_objects OWNER TO ams;

--
-- Name: farm_zones; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.farm_zones (
    id character varying(20) NOT NULL,
    name character varying(120) NOT NULL,
    risk_level character varying(20) NOT NULL,
    farm_id character varying(20),
    template_id character varying(24),
    template_zone_id character varying(24),
    zone_code character varying(40) NOT NULL,
    zone_category character varying(40) NOT NULL,
    biosecurity_level character varying(20) NOT NULL,
    layout_x double precision,
    layout_y double precision,
    layout_w double precision,
    layout_h double precision,
    sort_order integer NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public.farm_zones OWNER TO ams;

--
-- Name: farms; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.farms (
    id character varying(20) NOT NULL,
    name character varying(120) NOT NULL,
    location character varying(160) NOT NULL,
    plan character varying(40) NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.farms OWNER TO ams;

--
-- Name: licenses; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.licenses (
    id character varying(24) NOT NULL,
    farm_id character varying(20) NOT NULL,
    plan character varying(40) NOT NULL,
    max_cameras integer NOT NULL,
    max_ai_models integer NOT NULL,
    start_date character varying(20) NOT NULL,
    end_date character varying(20) NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.licenses OWNER TO ams;

--
-- Name: notification_gateways; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.notification_gateways (
    id character varying(24) NOT NULL,
    farm_id character varying(20) NOT NULL,
    gateway_type character varying(30) NOT NULL,
    endpoint character varying(255) NOT NULL,
    enabled boolean NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.notification_gateways OWNER TO ams;

--
-- Name: notification_rules; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.notification_rules (
    id character varying(20) NOT NULL,
    name character varying(120) NOT NULL,
    alert_category character varying(80) NOT NULL,
    severity character varying(20) NOT NULL,
    email boolean NOT NULL,
    telegram boolean NOT NULL,
    zalo boolean NOT NULL,
    enabled boolean NOT NULL
);


ALTER TABLE public.notification_rules OWNER TO ams;

--
-- Name: object_tracks; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.object_tracks (
    id character varying(32) NOT NULL,
    track_id integer NOT NULL,
    camera_id character varying(20) NOT NULL,
    object_type character varying(40) NOT NULL,
    current_zone character varying(40) NOT NULL,
    previous_zone character varying(40),
    employee_id character varying(24),
    enter_time character varying(32) NOT NULL,
    leave_time character varying(32),
    last_seen character varying(32) NOT NULL,
    confidence double precision NOT NULL
);


ALTER TABLE public.object_tracks OWNER TO ams;

--
-- Name: person_tracks; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.person_tracks (
    id character varying(32) NOT NULL,
    track_id integer NOT NULL,
    camera_id character varying(20) NOT NULL,
    zone_id character varying(40) NOT NULL,
    enter_time character varying(32) NOT NULL,
    exit_time character varying(32)
);


ALTER TABLE public.person_tracks OWNER TO ams;

--
-- Name: template_zone_definitions; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.template_zone_definitions (
    id character varying(24) NOT NULL,
    template_id character varying(24) NOT NULL,
    zone_code character varying(40) NOT NULL,
    zone_name character varying(120) NOT NULL,
    zone_category character varying(40) NOT NULL,
    biosecurity_level character varying(20) NOT NULL,
    risk_level character varying(20) NOT NULL,
    color character varying(20) NOT NULL,
    layout_x double precision NOT NULL,
    layout_y double precision NOT NULL,
    layout_w double precision NOT NULL,
    layout_h double precision NOT NULL,
    sort_order integer NOT NULL
);


ALTER TABLE public.template_zone_definitions OWNER TO ams;

--
-- Name: token_blacklist; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.token_blacklist (
    jti character varying(64) NOT NULL,
    user_id character varying(20) NOT NULL,
    expires_at integer NOT NULL
);


ALTER TABLE public.token_blacklist OWNER TO ams;

--
-- Name: track_workflow_progress; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.track_workflow_progress (
    id character varying(48) NOT NULL,
    track_id integer NOT NULL,
    camera_id character varying(20) NOT NULL,
    workflow_id character varying(24) NOT NULL,
    completed_step_order integer NOT NULL,
    last_zone character varying(40) NOT NULL,
    updated_at character varying(32) NOT NULL
);


ALTER TABLE public.track_workflow_progress OWNER TO ams;

--
-- Name: users; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.users (
    id character varying(20) NOT NULL,
    email character varying(160) NOT NULL,
    full_name character varying(120) NOT NULL,
    role character varying(60) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.users OWNER TO ams;

--
-- Name: visitors; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.visitors (
    id character varying(24) NOT NULL,
    visitor_name character varying(120) NOT NULL,
    company character varying(120) NOT NULL,
    vehicle_plate character varying(20) NOT NULL,
    visit_purpose character varying(255) NOT NULL,
    arrival_time character varying(32),
    departure_time character varying(32),
    approved_by character varying(120) NOT NULL
);


ALTER TABLE public.visitors OWNER TO ams;

--
-- Name: workflow_steps; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.workflow_steps (
    id character varying(24) NOT NULL,
    workflow_id character varying(24) NOT NULL,
    step_order integer NOT NULL,
    step_name character varying(120) NOT NULL,
    zone_code character varying(40) NOT NULL,
    required boolean DEFAULT true NOT NULL
);


ALTER TABLE public.workflow_steps OWNER TO ams;

--
-- Name: workflows; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.workflows (
    id character varying(24) NOT NULL,
    name character varying(160) NOT NULL,
    description text NOT NULL,
    object_type character varying(40) NOT NULL,
    enabled boolean NOT NULL,
    created_at character varying(32) NOT NULL
);


ALTER TABLE public.workflows OWNER TO ams;

--
-- Name: zone_polygons; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.zone_polygons (
    id character varying(24) NOT NULL,
    farm_id character varying(20) NOT NULL,
    camera_id character varying(20) NOT NULL,
    zone_name character varying(120) NOT NULL,
    zone_type character varying(40) NOT NULL,
    color character varying(20) NOT NULL,
    polygon_points json NOT NULL,
    active boolean NOT NULL,
    created_at character varying(32) NOT NULL,
    biosecurity_level character varying(20) NOT NULL
);


ALTER TABLE public.zone_polygons OWNER TO ams;

--
-- Name: zone_transitions; Type: TABLE; Schema: public; Owner: ams
--

CREATE TABLE public.zone_transitions (
    id character varying(28) NOT NULL,
    object_type character varying(40) NOT NULL,
    track_id integer NOT NULL,
    from_zone character varying(40) NOT NULL,
    to_zone character varying(40) NOT NULL,
    "timestamp" character varying(32) NOT NULL,
    camera_id character varying(20) NOT NULL,
    cross_time character varying(32) NOT NULL
);


ALTER TABLE public.zone_transitions OWNER TO ams;

--
-- Data for Name: ai_models; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.ai_models (id, model_name, model_type, version, enabled) FROM stdin;
AIM-001	AMS PPE Detector	improper_clothing	1.2.0	t
AIM-002	AMS Restricted Zone Intrusion	restricted_zone_intrusion	1.2.0	t
AIM-003	AMS Pig Fever Thermal	pig_fever	1.1.3	t
AIM-004	AMS Pig Abnormal Behavior	pig_abnormal	1.0.8	t
AIM-005	AMS Vehicle Disinfection Check	vehicle_disinfection	1.0.2	t
AIM-006	AMS Camera Health Monitor	camera_offline	1.2.0	t
\.


--
-- Data for Name: ai_tasks; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.ai_tasks (id, camera_id, category, status, priority, result, created_at, processed_at) FROM stdin;
TASK-SEED-001	CAM-001	improper_clothing	completed	10	{"source": "seed", "confidence": 84, "event_id": "EVT-001"}	2026-06-17T08:00:00+07:00	2026-06-17T08:00:05+07:00
TASK-SEED-002	CAM-002	restricted_zone_intrusion	completed	9	{"source": "seed", "confidence": 85, "event_id": "EVT-002"}	2026-06-17T09:00:00+07:00	2026-06-17T09:00:05+07:00
TASK-SEED-003	CAM-003	pig_fever	completed	8	{"source": "seed", "confidence": 86, "event_id": "EVT-003"}	2026-06-17T10:00:00+07:00	2026-06-17T10:00:05+07:00
TASK-SEED-004	CAM-004	pig_abnormal	completed	7	{"source": "seed", "confidence": 87, "event_id": "EVT-004"}	2026-06-17T11:00:00+07:00	2026-06-17T11:00:05+07:00
TASK-SEED-005	CAM-005	vehicle_disinfection	completed	6	{"source": "seed", "confidence": 88, "event_id": "EVT-005"}	2026-06-17T12:00:00+07:00	2026-06-17T12:00:05+07:00
TASK-SEED-006	CAM-006	camera_offline	completed	5	{"source": "seed", "confidence": 89, "event_id": "EVT-006"}	2026-06-17T13:00:00+07:00	2026-06-17T13:00:05+07:00
TASK-A6573A79DA	CAM-001	restricted_zone_intrusion	completed	10	{"event_id": "EVT-RT-BFC14B09", "snapshot_id": "SNP-RT-E18F89D8", "notification": "triggered", "confidence": 89}	2026-06-17T10:05:20.421913+00:00	2026-06-17T10:05:20.428434+00:00
TASK-RT-1041656A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-ABAB9E7D", "snapshot_id": "SNP-RT-0DB16962", "notification": "triggered", "confidence": 94}	2026-06-17T10:05:36.003501+00:00	2026-06-17T10:05:36.019038+00:00
TASK-RT-F59EC88E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6BB404E1", "snapshot_id": "SNP-RT-50F07727", "notification": "triggered", "confidence": 93}	2026-06-17T10:06:39.517885+00:00	2026-06-17T10:06:39.553970+00:00
TASK-RT-899057AD	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-9599DF0C", "snapshot_id": "SNP-RT-833A090A", "notification": "triggered", "confidence": 94}	2026-06-17T10:07:09.567092+00:00	2026-06-17T10:07:09.597718+00:00
TASK-RT-0EE844EF	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-E338BA34", "snapshot_id": "SNP-RT-677B91EC", "notification": "triggered", "confidence": 89}	2026-06-17T10:07:39.609606+00:00	2026-06-17T10:07:39.628635+00:00
TASK-RT-0E51FA97	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-70D6A36E", "snapshot_id": "SNP-RT-C4A7AF0F", "notification": "triggered", "confidence": 98}	2026-06-17T10:08:09.651765+00:00	2026-06-17T10:08:09.672932+00:00
TASK-RT-CB24EF83	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-A5AD8924", "snapshot_id": "SNP-RT-1B431BAA", "notification": "triggered", "confidence": 99}	2026-06-17T10:08:39.686085+00:00	2026-06-17T10:08:39.708731+00:00
TASK-RT-7DCC3DB4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9277B021", "snapshot_id": "SNP-RT-39E7F534", "notification": "triggered", "confidence": 89}	2026-06-17T10:09:09.719678+00:00	2026-06-17T10:09:09.743585+00:00
TASK-RT-2D4AC891	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-9A030D8C", "snapshot_id": "SNP-RT-39BFF036", "notification": "triggered", "confidence": 89}	2026-06-17T10:09:39.758633+00:00	2026-06-17T10:09:39.788975+00:00
TASK-RT-9EEAAF89	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-34FB34CF", "snapshot_id": "SNP-RT-35CAFBC6", "notification": "triggered", "confidence": 99}	2026-06-17T10:10:09.801340+00:00	2026-06-17T10:10:09.827674+00:00
TASK-RT-08E282E6	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-C46862AA", "snapshot_id": "SNP-RT-1487B010", "notification": "triggered", "confidence": 90}	2026-06-17T10:10:39.840035+00:00	2026-06-17T10:10:39.858404+00:00
TASK-RT-21EF091B	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-927CC36B", "snapshot_id": "SNP-RT-F6F3D5D2", "notification": "triggered", "confidence": 89}	2026-06-17T10:11:09.865479+00:00	2026-06-17T10:11:09.881509+00:00
TASK-RT-EC86A85C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-876895A2", "snapshot_id": "SNP-RT-7F2A5C87", "notification": "triggered", "confidence": 96}	2026-06-17T10:11:39.890853+00:00	2026-06-17T10:11:39.906509+00:00
TASK-RT-A45F448B	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-2D922793", "snapshot_id": "SNP-RT-B7F0A587", "notification": "triggered", "confidence": 99}	2026-06-17T10:12:09.919277+00:00	2026-06-17T10:12:09.937592+00:00
TASK-RT-0F5EB290	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-C423F422", "snapshot_id": "SNP-RT-FB84D30A", "notification": "triggered", "confidence": 90}	2026-06-17T10:12:39.947451+00:00	2026-06-17T10:12:39.955093+00:00
TASK-E9EDF1D13C	CAM-002	pig_fever	completed	9	{"event_id": "EVT-RT-DE295378", "snapshot_id": "SNP-RT-22114E02", "notification": "triggered", "confidence": 90}	2026-06-17T10:13:30.129338+00:00	2026-06-17T10:13:30.136965+00:00
TASK-RT-2502BDA3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-02F7DF6A", "snapshot_id": "SNP-RT-1A7DB589", "notification": "triggered", "confidence": 99}	2026-06-17T10:13:46.574094+00:00	2026-06-17T10:13:46.591503+00:00
TASK-E12DB6E3C8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E3500358", "snapshot_id": "SNP-RT-01668253", "notification": "triggered", "confidence": 97}	2026-06-17T10:39:51.540518+00:00	2026-06-17T10:39:51.621664+00:00
TASK-BD07C36E20	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-08DE7C83", "snapshot_id": "SNP-RT-4756FC06", "notification": "triggered", "confidence": 88}	2026-06-17T10:40:02.613360+00:00	2026-06-17T10:40:02.624466+00:00
TASK-207C21B740	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-17B29287", "snapshot_id": "SNP-RT-B9953C15", "notification": "triggered", "confidence": 91}	2026-06-17T10:40:21.714144+00:00	2026-06-17T10:40:21.731465+00:00
TASK-820FC47E53	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-81276D8F", "snapshot_id": "SNP-RT-B7D73998", "notification": "triggered", "confidence": 92}	2026-06-17T10:40:51.815802+00:00	2026-06-17T10:40:51.825826+00:00
TASK-SEED-009	CAM-009	improper_clothing	queued	8	{"source": "seed", "confidence": 92, "event_id": null}	2026-06-17T16:00:00+07:00	\N
TASK-9516EAB9D0	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-CEC94A75", "snapshot_id": "SNP-RT-4488BA09", "notification": "triggered", "confidence": 96}	2026-06-17T10:41:22.009078+00:00	2026-06-17T10:41:22.072597+00:00
TASK-D4498DD574	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3D1B30D7", "snapshot_id": "SNP-RT-0F14A9B3", "notification": "triggered", "confidence": 89}	2026-06-17T10:41:52.240355+00:00	2026-06-17T10:41:52.334133+00:00
TASK-C393999C2C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BAE6E1D7", "snapshot_id": "SNP-RT-AEDC5B77", "notification": "triggered", "confidence": 97}	2026-06-17T10:42:22.436866+00:00	2026-06-17T10:42:22.456738+00:00
TASK-77218524C2	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-84A7C1CC", "snapshot_id": "SNP-RT-FB3141A1", "notification": "triggered", "confidence": 92}	2026-06-17T10:42:52.543373+00:00	2026-06-17T10:42:52.567087+00:00
TASK-09F24396AB	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8E95A8E7", "snapshot_id": "SNP-RT-BEBF895E", "notification": "triggered", "confidence": 98}	2026-06-17T10:43:22.654560+00:00	2026-06-17T10:43:22.668123+00:00
TASK-9341FBCCF9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9BD213BC", "snapshot_id": "SNP-RT-E191AF81", "notification": "triggered", "confidence": 98}	2026-06-17T10:43:52.749930+00:00	2026-06-17T10:43:52.770134+00:00
TASK-98B47A3F46	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6D08308D", "snapshot_id": "SNP-RT-9126DA26", "notification": "triggered", "confidence": 93}	2026-06-17T10:44:22.825826+00:00	2026-06-17T10:44:22.837239+00:00
TASK-91BEE9064E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D466ABAC", "snapshot_id": "SNP-RT-48B03081", "notification": "triggered", "confidence": 99}	2026-06-17T10:44:52.932469+00:00	2026-06-17T10:44:52.953629+00:00
TASK-6C3A429B55	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-AC0705AD", "snapshot_id": "SNP-RT-CB8F77E0", "notification": "triggered", "confidence": 93}	2026-06-17T10:45:23.035671+00:00	2026-06-17T10:45:23.054568+00:00
TASK-D6632352AA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-915DA336", "snapshot_id": "SNP-RT-CC6A91DE", "notification": "triggered", "confidence": 90}	2026-06-17T10:45:53.142511+00:00	2026-06-17T10:45:53.161129+00:00
TASK-936BE1AED3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6B65B8F0", "snapshot_id": "SNP-RT-4EB86ACB", "notification": "triggered", "confidence": 90}	2026-06-17T10:46:23.236041+00:00	2026-06-17T10:46:23.256155+00:00
TASK-08B63B76E0	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BD626578", "snapshot_id": "SNP-RT-9309CD64", "notification": "triggered", "confidence": 99}	2026-06-17T10:46:53.346467+00:00	2026-06-17T10:46:53.362602+00:00
TASK-B5B2BAA16F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BE27BDC6", "snapshot_id": "SNP-RT-0D3DE2B0", "notification": "triggered", "confidence": 99}	2026-06-17T10:47:23.453811+00:00	2026-06-17T10:47:23.473711+00:00
TASK-DFDB43D4EA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-73006EA4", "snapshot_id": "SNP-RT-7B782F3D", "notification": "triggered", "confidence": 98}	2026-06-17T10:47:53.554988+00:00	2026-06-17T10:47:53.575527+00:00
TASK-5C1594D82C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A480BC66", "snapshot_id": "SNP-RT-51D2EB19", "notification": "triggered", "confidence": 89}	2026-06-17T10:48:23.649894+00:00	2026-06-17T10:48:23.664584+00:00
TASK-D48FE37DA7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6A2EEA15", "snapshot_id": "SNP-RT-5513A9A8", "notification": "triggered", "confidence": 90}	2026-06-17T10:48:53.756623+00:00	2026-06-17T10:48:53.771802+00:00
TASK-7CA7C54C38	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7A471A36", "snapshot_id": "SNP-RT-2701EAEE", "notification": "triggered", "confidence": 93}	2026-06-17T10:49:23.867387+00:00	2026-06-17T10:49:23.890381+00:00
TASK-04DD1E403D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A578B0E9", "snapshot_id": "SNP-RT-F9D2AA67", "notification": "triggered", "confidence": 95}	2026-06-17T10:49:53.979228+00:00	2026-06-17T10:49:53.996071+00:00
TASK-F97EB49B88	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9FF2F5FA", "snapshot_id": "SNP-RT-747E79C9", "notification": "triggered", "confidence": 92}	2026-06-17T10:50:24.067310+00:00	2026-06-17T10:50:24.084807+00:00
TASK-26DC58A60F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D1863B4B", "snapshot_id": "SNP-RT-2582CCFD", "notification": "triggered", "confidence": 93}	2026-06-17T10:50:54.168339+00:00	2026-06-17T10:50:54.182935+00:00
TASK-317E4AD58E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F0842F88", "snapshot_id": "SNP-RT-DC9FF292", "notification": "triggered", "confidence": 91}	2026-06-17T10:51:24.279227+00:00	2026-06-17T10:51:24.299473+00:00
TASK-5B87C1C8B1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-DF66D38B", "snapshot_id": "SNP-RT-92486101", "notification": "triggered", "confidence": 94}	2026-06-17T10:51:54.396765+00:00	2026-06-17T10:51:54.416531+00:00
TASK-835B9F7C22	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7C31CBAF", "snapshot_id": "SNP-RT-09A4C2B0", "notification": "triggered", "confidence": 99}	2026-06-17T10:52:24.547179+00:00	2026-06-17T10:52:24.602881+00:00
TASK-EA10D36956	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-5BCE2E00", "snapshot_id": "SNP-RT-E03AD713", "notification": "triggered", "confidence": 96}	2026-06-17T10:52:54.695014+00:00	2026-06-17T10:52:54.711343+00:00
TASK-780076B84E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D193DAD9", "snapshot_id": "SNP-RT-3574621F", "notification": "triggered", "confidence": 91}	2026-06-17T10:53:24.790679+00:00	2026-06-17T10:53:24.807725+00:00
TASK-63E7A2B3DF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B8FA3700", "snapshot_id": "SNP-RT-E27ED637", "notification": "triggered", "confidence": 93}	2026-06-17T10:53:54.897879+00:00	2026-06-17T10:53:54.919056+00:00
TASK-4515C540F4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-21536871", "snapshot_id": "SNP-RT-A58976C4", "notification": "triggered", "confidence": 93}	2026-06-17T10:54:24.998609+00:00	2026-06-17T10:54:25.013666+00:00
TASK-AA1991BBE1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-FA3F75F4", "snapshot_id": "SNP-RT-B6E85CBE", "notification": "triggered", "confidence": 99}	2026-06-17T10:54:55.112584+00:00	2026-06-17T10:54:55.132581+00:00
TASK-D077839DC1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-CC39D3BF", "snapshot_id": "SNP-RT-C8FA1717", "notification": "triggered", "confidence": 97}	2026-06-17T10:55:25.225115+00:00	2026-06-17T10:55:25.244268+00:00
TASK-25620BC7C9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8FC08AB1", "snapshot_id": "SNP-RT-D7AC0941", "notification": "triggered", "confidence": 91}	2026-06-17T10:55:55.307999+00:00	2026-06-17T10:55:55.324131+00:00
TASK-C7CD3337CC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6496304B", "snapshot_id": "SNP-RT-D6FB9A5A", "notification": "triggered", "confidence": 92}	2026-06-17T10:56:25.430878+00:00	2026-06-17T10:56:25.449874+00:00
TASK-29218EF9C4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-58C22B56", "snapshot_id": "SNP-RT-D6CB3AEC", "notification": "triggered", "confidence": 97}	2026-06-17T10:56:55.531269+00:00	2026-06-17T10:56:55.550523+00:00
TASK-82E23A4ED7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8C2CD6F7", "snapshot_id": "SNP-RT-32C3A2C8", "notification": "triggered", "confidence": 95}	2026-06-17T10:57:25.634904+00:00	2026-06-17T10:57:25.655026+00:00
TASK-9E51F1F881	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-34B0B646", "snapshot_id": "SNP-RT-1D0507D0", "notification": "triggered", "confidence": 99}	2026-06-17T10:57:55.762175+00:00	2026-06-17T10:57:55.776702+00:00
TASK-4E14B2540F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-FAE1F3A6", "snapshot_id": "SNP-RT-834A4752", "notification": "triggered", "confidence": 93}	2026-06-17T10:58:25.869241+00:00	2026-06-17T10:58:25.885974+00:00
TASK-6353F4A1B5	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E5959412", "snapshot_id": "SNP-RT-C7D6E2BB", "notification": "triggered", "confidence": 91}	2026-06-17T10:58:55.942615+00:00	2026-06-17T10:58:55.950266+00:00
TASK-E6095BAA3B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-189AD3CF", "snapshot_id": "SNP-RT-D0CCD12E", "notification": "triggered", "confidence": 89}	2026-06-17T10:59:26.041196+00:00	2026-06-17T10:59:26.060144+00:00
TASK-2A8CEE8D61	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-15B5B56B", "snapshot_id": "SNP-RT-0BCB4AE0", "notification": "triggered", "confidence": 92}	2026-06-17T10:59:56.127077+00:00	2026-06-17T10:59:56.133700+00:00
TASK-AC1CE2D93D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-62048F22", "snapshot_id": "SNP-RT-352D8782", "notification": "triggered", "confidence": 93}	2026-06-17T11:00:26.214844+00:00	2026-06-17T11:00:26.236470+00:00
TASK-ED492622C8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B2331059", "snapshot_id": "SNP-RT-66B53F41", "notification": "triggered", "confidence": 97}	2026-06-17T11:00:56.295516+00:00	2026-06-17T11:00:56.302703+00:00
TASK-013C1B324E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A58C4061", "snapshot_id": "SNP-RT-01EA45B8", "notification": "triggered", "confidence": 96}	2026-06-17T11:01:26.389753+00:00	2026-06-17T11:01:26.414350+00:00
TASK-277985458D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-21821EFE", "snapshot_id": "SNP-RT-5ACBBE93", "notification": "triggered", "confidence": 91}	2026-06-17T11:01:56.494958+00:00	2026-06-17T11:01:56.509249+00:00
TASK-83E6177CCC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-EAFE0103", "snapshot_id": "SNP-RT-50AB5946", "notification": "triggered", "confidence": 99}	2026-06-17T11:02:26.564530+00:00	2026-06-17T11:02:26.572128+00:00
TASK-FA5D95E264	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3CD59E0A", "snapshot_id": "SNP-RT-E92EA25B", "notification": "triggered", "confidence": 94}	2026-06-17T11:02:56.655091+00:00	2026-06-17T11:02:56.677088+00:00
TASK-7B0C68613E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8CB0CFDE", "snapshot_id": "SNP-RT-AF7ADE53", "notification": "triggered", "confidence": 92}	2026-06-17T11:03:26.759219+00:00	2026-06-17T11:03:26.780180+00:00
TASK-F91C0F5E9B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-035FC18A", "snapshot_id": "SNP-RT-07CB56D7", "notification": "triggered", "confidence": 98}	2026-06-17T11:03:56.866369+00:00	2026-06-17T11:03:56.882373+00:00
TASK-2D5947470E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8B98E8F6", "snapshot_id": "SNP-RT-C9EE7BC5", "notification": "triggered", "confidence": 94}	2026-06-17T11:04:26.983787+00:00	2026-06-17T11:04:27.000738+00:00
TASK-669830D189	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A62E7420", "snapshot_id": "SNP-RT-13331A81", "notification": "triggered", "confidence": 89}	2026-06-17T11:04:57.089152+00:00	2026-06-17T11:04:57.107395+00:00
TASK-40683AB350	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-890B4B35", "snapshot_id": "SNP-RT-879620AA", "notification": "triggered", "confidence": 99}	2026-06-17T11:05:27.198448+00:00	2026-06-17T11:05:27.215784+00:00
TASK-4E1B813CDA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BD7B3FFD", "snapshot_id": "SNP-RT-78760BA7", "notification": "triggered", "confidence": 90}	2026-06-17T11:05:57.298256+00:00	2026-06-17T11:05:57.314639+00:00
TASK-152291AED0	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4C51ED30", "snapshot_id": "SNP-RT-138DE4A2", "notification": "triggered", "confidence": 89}	2026-06-17T11:06:27.408375+00:00	2026-06-17T11:06:27.424493+00:00
TASK-12350C6A80	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F76AD84A", "snapshot_id": "SNP-RT-7DDF2F33", "notification": "triggered", "confidence": 91}	2026-06-17T11:06:57.508722+00:00	2026-06-17T11:06:57.526089+00:00
TASK-F636EDB4D9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-0528AC11", "snapshot_id": "SNP-RT-42507479", "notification": "triggered", "confidence": 97}	2026-06-17T11:07:27.619901+00:00	2026-06-17T11:07:27.632038+00:00
TASK-7BFDBD476D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-AB639D38", "snapshot_id": "SNP-RT-AD367C46", "notification": "triggered", "confidence": 93}	2026-06-17T11:07:57.687845+00:00	2026-06-17T11:07:57.711335+00:00
TASK-87BF29548D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-01B855E7", "snapshot_id": "SNP-RT-047502A6", "notification": "triggered", "confidence": 95}	2026-06-17T11:08:27.786909+00:00	2026-06-17T11:08:27.811917+00:00
TASK-7D0CB2B0C6	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D11FA1B5", "snapshot_id": "SNP-RT-33E3E69C", "notification": "triggered", "confidence": 93}	2026-06-17T11:08:57.892041+00:00	2026-06-17T11:08:57.905540+00:00
TASK-BEE58C9E8B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BDD8026A", "snapshot_id": "SNP-RT-8125A032", "notification": "triggered", "confidence": 95}	2026-06-17T11:09:28.074344+00:00	2026-06-17T11:09:28.088208+00:00
TASK-62D947DFEA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7E9F006D", "snapshot_id": "SNP-RT-82A17860", "notification": "triggered", "confidence": 96}	2026-06-17T11:09:58.173073+00:00	2026-06-17T11:09:58.184726+00:00
TASK-D1CE2CC918	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9B32B69A", "snapshot_id": "SNP-RT-6DA590DF", "notification": "triggered", "confidence": 92}	2026-06-17T11:10:28.255998+00:00	2026-06-17T11:10:28.276326+00:00
TASK-CC7D15B8EE	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7ACE6473", "snapshot_id": "SNP-RT-9BBC7994", "notification": "triggered", "confidence": 97}	2026-06-17T11:10:58.352482+00:00	2026-06-17T11:10:58.364475+00:00
TASK-3061CEA756	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D5061419", "snapshot_id": "SNP-RT-C97B3054", "notification": "triggered", "confidence": 91}	2026-06-17T11:11:28.429688+00:00	2026-06-17T11:11:28.441368+00:00
TASK-85711E85ED	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1ABFE50B", "snapshot_id": "SNP-RT-11CBB77D", "notification": "triggered", "confidence": 88}	2026-06-17T11:11:58.557459+00:00	2026-06-17T11:11:58.587262+00:00
TASK-647436C5E5	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4C60F9CC", "snapshot_id": "SNP-RT-43FE1A39", "notification": "triggered", "confidence": 92}	2026-06-17T11:12:28.674115+00:00	2026-06-17T11:12:28.694105+00:00
TASK-23AAD58DB7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F7C36D50", "snapshot_id": "SNP-RT-16AC0BD0", "notification": "triggered", "confidence": 96}	2026-06-17T11:12:58.775070+00:00	2026-06-17T11:12:58.790527+00:00
TASK-EF392AD9CF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-666372AF", "snapshot_id": "SNP-RT-C3614D82", "notification": "triggered", "confidence": 97}	2026-06-17T11:13:28.873624+00:00	2026-06-17T11:13:28.891697+00:00
TASK-8E2118A0DF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F190C297", "snapshot_id": "SNP-RT-F6C034B1", "notification": "triggered", "confidence": 94}	2026-06-17T11:13:58.982276+00:00	2026-06-17T11:13:58.997879+00:00
TASK-A93F02AA41	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8B9E19CA", "snapshot_id": "SNP-RT-B1053058", "notification": "triggered", "confidence": 90}	2026-06-17T11:14:29.057525+00:00	2026-06-17T11:14:29.071967+00:00
TASK-96FA9124A1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8928E2BF", "snapshot_id": "SNP-RT-301B1892", "notification": "triggered", "confidence": 90}	2026-06-17T11:14:59.160138+00:00	2026-06-17T11:14:59.173603+00:00
TASK-5CADBC0793	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1E3F177D", "snapshot_id": "SNP-RT-9BA6FB50", "notification": "triggered", "confidence": 88}	2026-06-17T11:15:29.258852+00:00	2026-06-17T11:15:29.278994+00:00
TASK-935C14BC85	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-742BC921", "snapshot_id": "SNP-RT-78798827", "notification": "triggered", "confidence": 88}	2026-06-17T11:15:59.352968+00:00	2026-06-17T11:15:59.366964+00:00
TASK-8B84B3B8EB	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1601262E", "snapshot_id": "SNP-RT-4F93D708", "notification": "triggered", "confidence": 93}	2026-06-17T11:16:29.440433+00:00	2026-06-17T11:16:29.456080+00:00
TASK-A2D4F9E1C9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-005247E1", "snapshot_id": "SNP-RT-A58F1E66", "notification": "triggered", "confidence": 93}	2026-06-17T11:16:59.523317+00:00	2026-06-17T11:16:59.538560+00:00
TASK-65039ECF1D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-46EDDC05", "snapshot_id": "SNP-RT-E8BE3695", "notification": "triggered", "confidence": 99}	2026-06-17T11:17:29.648369+00:00	2026-06-17T11:17:29.667193+00:00
TASK-64444D7A46	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B49D9895", "snapshot_id": "SNP-RT-D29926B9", "notification": "triggered", "confidence": 90}	2026-06-17T11:17:59.750906+00:00	2026-06-17T11:17:59.774077+00:00
TASK-FA40254546	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-40E7E3F0", "snapshot_id": "SNP-RT-5C8F5F59", "notification": "triggered", "confidence": 97}	2026-06-17T11:18:29.861392+00:00	2026-06-17T11:18:29.875438+00:00
TASK-F044EC8265	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F925007A", "snapshot_id": "SNP-RT-12A0F44C", "notification": "triggered", "confidence": 99}	2026-06-17T11:18:59.975372+00:00	2026-06-17T11:18:59.991660+00:00
TASK-8FAD9152F2	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-983B7A3E", "snapshot_id": "SNP-RT-9A45DCEF", "notification": "triggered", "confidence": 89}	2026-06-17T11:19:30.081183+00:00	2026-06-17T11:19:30.092595+00:00
TASK-5C96C47F08	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-0E648378", "snapshot_id": "SNP-RT-03D631D2", "notification": "triggered", "confidence": 94}	2026-06-17T11:20:00.189286+00:00	2026-06-17T11:20:00.203561+00:00
TASK-RT-B87C74B3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-97ADA9F5", "snapshot_id": "SNP-RT-7AFD36E7", "notification": "triggered", "confidence": 90}	2026-06-17T11:20:17.048169+00:00	2026-06-17T11:20:17.067348+00:00
TASK-AE74154D8E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-11BCF260", "snapshot_id": "SNP-RT-BE9722E5", "notification": "triggered", "confidence": 97}	2026-06-17T11:20:30.300099+00:00	2026-06-17T11:20:30.314439+00:00
TASK-RT-BD19D809	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-28A01B9D", "snapshot_id": "SNP-RT-EF09EE99", "notification": "triggered", "confidence": 96}	2026-06-17T11:20:47.080036+00:00	2026-06-17T11:20:47.108960+00:00
TASK-5DC0593237	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-46EBB3F8", "snapshot_id": "SNP-RT-B7C66EC8", "notification": "triggered", "confidence": 99}	2026-06-17T11:21:00.406670+00:00	2026-06-17T11:21:00.419373+00:00
TASK-RT-DB9384BA	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-0329AF4A", "snapshot_id": "SNP-RT-D9140C50", "notification": "triggered", "confidence": 94}	2026-06-17T11:21:17.125050+00:00	2026-06-17T11:21:17.156955+00:00
TASK-2250DF1189	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B1BF2656", "snapshot_id": "SNP-RT-6A3D4AA5", "notification": "triggered", "confidence": 96}	2026-06-17T11:21:30.465584+00:00	2026-06-17T11:21:30.469836+00:00
TASK-RT-D42AEB8C	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-5A0D2CAB", "snapshot_id": "SNP-RT-6F4AAD48", "notification": "triggered", "confidence": 93}	2026-06-17T11:21:47.169614+00:00	2026-06-17T11:21:47.189710+00:00
TASK-8133D08A62	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1C75A8AC", "snapshot_id": "SNP-RT-B55B0A6F", "notification": "triggered", "confidence": 93}	2026-06-17T11:22:00.528486+00:00	2026-06-17T11:22:00.533261+00:00
TASK-RT-CB763AB0	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-AE169985", "snapshot_id": "SNP-RT-F2D9AE1A", "notification": "triggered", "confidence": 98}	2026-06-17T11:22:17.201290+00:00	2026-06-17T11:22:17.226792+00:00
TASK-7A5AB65D64	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-445037A6", "snapshot_id": "SNP-RT-96C47431", "notification": "triggered", "confidence": 94}	2026-06-17T11:22:30.595751+00:00	2026-06-17T11:22:30.607188+00:00
TASK-RT-1E0E5AF4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1F2382FF", "snapshot_id": "SNP-RT-BAF4BB63", "notification": "triggered", "confidence": 96}	2026-06-17T11:22:47.237930+00:00	2026-06-17T11:22:47.259737+00:00
TASK-5D9DEAE6EE	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A9415D69", "snapshot_id": "SNP-RT-552FF62D", "notification": "triggered", "confidence": 98}	2026-06-17T11:23:00.698886+00:00	2026-06-17T11:23:00.715219+00:00
TASK-RT-E26A88E1	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-0AC67C31", "snapshot_id": "SNP-RT-BDE0508E", "notification": "triggered", "confidence": 96}	2026-06-17T11:23:17.270227+00:00	2026-06-17T11:23:17.288273+00:00
TASK-16911A5C6C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3D7175A3", "snapshot_id": "SNP-RT-471195EF", "notification": "triggered", "confidence": 89}	2026-06-17T11:23:30.811185+00:00	2026-06-17T11:23:30.825099+00:00
TASK-RT-577EEE46	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-DD971EF9", "snapshot_id": "SNP-RT-47A4B21A", "notification": "triggered", "confidence": 95}	2026-06-17T11:23:47.296703+00:00	2026-06-17T11:23:47.319252+00:00
TASK-C962B5E77B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-79C9E74E", "snapshot_id": "SNP-RT-65F7FC3B", "notification": "triggered", "confidence": 99}	2026-06-17T11:24:00.886874+00:00	2026-06-17T11:24:00.906675+00:00
TASK-RT-36CEF3C5	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-6CBA8F56", "snapshot_id": "SNP-RT-8B00993E", "notification": "triggered", "confidence": 95}	2026-06-17T11:24:17.330736+00:00	2026-06-17T11:24:17.345356+00:00
TASK-8655BF4A87	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-ABD6E01F", "snapshot_id": "SNP-RT-4F8A5560", "notification": "triggered", "confidence": 98}	2026-06-17T11:24:30.974352+00:00	2026-06-17T11:24:30.989615+00:00
TASK-RT-E27A994F	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-E3AECE57", "snapshot_id": "SNP-RT-9BFF1B77", "notification": "triggered", "confidence": 90}	2026-06-17T11:24:47.357468+00:00	2026-06-17T11:24:47.391625+00:00
TASK-9B06460DD1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E429A27B", "snapshot_id": "SNP-RT-507C8CBC", "notification": "triggered", "confidence": 88}	2026-06-17T11:25:01.074581+00:00	2026-06-17T11:25:01.090323+00:00
TASK-F13A7A6BF2	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-402E8448", "snapshot_id": "SNP-RT-7418ABA3", "notification": "triggered", "confidence": 95}	2026-06-17T11:25:10.518501+00:00	2026-06-17T11:25:10.522775+00:00
TASK-ED33AD45BF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1C4417FC", "snapshot_id": "SNP-RT-E3FBBF65", "notification": "triggered", "confidence": 93}	2026-06-17T11:25:15.230823+00:00	2026-06-17T11:25:15.236371+00:00
TASK-RT-32FF2DEF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-5AD44F56", "snapshot_id": "SNP-RT-28AF1EC1", "notification": "triggered", "confidence": 95}	2026-06-17T11:25:17.403732+00:00	2026-06-17T11:25:17.417642+00:00
TASK-7418397A61	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A85D7334", "snapshot_id": "SNP-RT-CC5C459A", "notification": "triggered", "confidence": 88}	2026-06-17T11:25:40.626236+00:00	2026-06-17T11:25:40.632914+00:00
TASK-RT-7C038A80	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-EEECA9BB", "snapshot_id": "SNP-RT-21567AED", "notification": "triggered", "confidence": 91}	2026-06-17T11:25:47.426098+00:00	2026-06-17T11:25:47.432577+00:00
TASK-A6D39E144D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-21B241FC", "snapshot_id": "SNP-RT-28C317A3", "notification": "triggered", "confidence": 94}	2026-06-17T11:26:10.731801+00:00	2026-06-17T11:26:10.739306+00:00
TASK-RT-C3D6A4F4	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-7D0161F8", "snapshot_id": "SNP-RT-15263731", "notification": "triggered", "confidence": 96}	2026-06-17T11:26:17.437769+00:00	2026-06-17T11:26:17.450581+00:00
TASK-DC3AA86377	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E15945A2", "snapshot_id": "SNP-RT-064E86A9", "notification": "triggered", "confidence": 97}	2026-06-17T11:26:40.846918+00:00	2026-06-17T11:26:40.852128+00:00
TASK-RT-A2C06663	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-F80A0D7A", "snapshot_id": "SNP-RT-D6074555", "notification": "triggered", "confidence": 99}	2026-06-17T11:26:47.467776+00:00	2026-06-17T11:26:47.491670+00:00
TASK-1D46A611E3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C4E974AE", "snapshot_id": "SNP-RT-86A0BE27", "notification": "triggered", "confidence": 96}	2026-06-17T11:27:10.920968+00:00	2026-06-17T11:27:10.927540+00:00
TASK-RT-D94A7836	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-1164035B", "snapshot_id": "SNP-RT-919FEC7B", "notification": "triggered", "confidence": 99}	2026-06-17T11:27:17.503899+00:00	2026-06-17T11:27:17.519382+00:00
TASK-D14F5D6E48	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-772E7897", "snapshot_id": "SNP-RT-3630F009", "notification": "triggered", "confidence": 92}	2026-06-17T11:27:41.022644+00:00	2026-06-17T11:27:41.033279+00:00
TASK-RT-94545492	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-0D4E4060", "snapshot_id": "SNP-RT-C5E34664", "notification": "triggered", "confidence": 96}	2026-06-17T11:27:47.530101+00:00	2026-06-17T11:27:47.553088+00:00
TASK-118ACB685C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-81925D12", "snapshot_id": "SNP-RT-8B7B7161", "notification": "triggered", "confidence": 88}	2026-06-17T11:28:11.125945+00:00	2026-06-17T11:28:11.130156+00:00
TASK-RT-9FB6A4D0	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-003CF0A2", "snapshot_id": "SNP-RT-3698940B", "notification": "triggered", "confidence": 98}	2026-06-17T11:28:17.566423+00:00	2026-06-17T11:28:17.581073+00:00
TASK-F87FAF486E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-613C495B", "snapshot_id": "SNP-RT-6BB862B5", "notification": "triggered", "confidence": 92}	2026-06-17T11:28:35.777029+00:00	2026-06-17T11:28:35.784519+00:00
TASK-DEE4732A2B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-73C67934", "snapshot_id": "SNP-RT-0FDA611B", "notification": "triggered", "confidence": 93}	2026-06-17T11:28:54.694707+00:00	2026-06-17T11:28:54.698117+00:00
TASK-ACF7351EB3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C99CEA05", "snapshot_id": "SNP-RT-E4925B7D", "notification": "triggered", "confidence": 97}	2026-06-17T11:28:54.745359+00:00	2026-06-17T11:28:54.749984+00:00
TASK-RT-A899BAE8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E81AE02E", "snapshot_id": "SNP-RT-0EEFABFB", "notification": "triggered", "confidence": 97}	2026-06-17T11:28:55.181209+00:00	2026-06-17T11:28:55.185606+00:00
TASK-2CAD34CF7E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D7AA35A8", "snapshot_id": "SNP-RT-82A0DD6A", "notification": "triggered", "confidence": 96}	2026-06-17T11:29:05.879921+00:00	2026-06-17T11:29:05.889117+00:00
TASK-RT-17064911	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-1E90893A", "snapshot_id": "SNP-RT-51C7ABF9", "notification": "triggered", "confidence": 92}	2026-06-17T11:29:25.199715+00:00	2026-06-17T11:29:25.231629+00:00
TASK-B55AB73EE3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-89A6EB4E", "snapshot_id": "SNP-RT-B1B69FDB", "notification": "triggered", "confidence": 90}	2026-06-17T11:29:36.015099+00:00	2026-06-17T11:29:36.028478+00:00
TASK-RT-F2C4D050	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-B6322AD7", "snapshot_id": "SNP-RT-83F4E235", "notification": "triggered", "confidence": 95}	2026-06-17T11:29:55.246189+00:00	2026-06-17T11:29:55.271933+00:00
TASK-8D1E15AE93	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D26A1E81", "snapshot_id": "SNP-RT-A3EA61AD", "notification": "triggered", "confidence": 91}	2026-06-17T11:30:06.146630+00:00	2026-06-17T11:30:06.150676+00:00
TASK-RT-E8D769B8	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-D689D0D3", "snapshot_id": "SNP-RT-0556E3D8", "notification": "triggered", "confidence": 94}	2026-06-17T11:30:25.287926+00:00	2026-06-17T11:30:25.313224+00:00
TASK-0A5B308039	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4317FDEB", "snapshot_id": "SNP-RT-2CC7057A", "notification": "triggered", "confidence": 94}	2026-06-17T11:30:36.252862+00:00	2026-06-17T11:30:36.258597+00:00
TASK-RT-528C005B	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-413A8029", "snapshot_id": "SNP-RT-5AA8AC1F", "notification": "triggered", "confidence": 88}	2026-06-17T11:30:55.327562+00:00	2026-06-17T11:30:55.354140+00:00
TASK-95D7A26B46	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2F01612B", "snapshot_id": "SNP-RT-C6D400A4", "notification": "triggered", "confidence": 92}	2026-06-17T11:31:06.350902+00:00	2026-06-17T11:31:06.358675+00:00
TASK-RT-2ABFFE98	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-02D41BB8", "snapshot_id": "SNP-RT-CE6250BF", "notification": "triggered", "confidence": 94}	2026-06-17T11:31:25.367184+00:00	2026-06-17T11:31:25.393155+00:00
TASK-DF5117DD75	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B12F7CA0", "snapshot_id": "SNP-RT-8192C1DC", "notification": "triggered", "confidence": 88}	2026-06-17T11:31:36.478012+00:00	2026-06-17T11:31:36.483764+00:00
TASK-RT-B115E8AE	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-138FD32B", "snapshot_id": "SNP-RT-A0421BA8", "notification": "triggered", "confidence": 89}	2026-06-17T11:31:55.418608+00:00	2026-06-17T11:31:55.460822+00:00
TASK-C7F223786D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-ECBF4A37", "snapshot_id": "SNP-RT-E2B3EEC9", "notification": "triggered", "confidence": 94}	2026-06-17T11:32:06.624477+00:00	2026-06-17T11:32:06.630922+00:00
TASK-RT-1E303225	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-76C289CD", "snapshot_id": "SNP-RT-FD4915EA", "notification": "triggered", "confidence": 93}	2026-06-17T11:32:25.483328+00:00	2026-06-17T11:32:25.502471+00:00
TASK-D6B2EC518C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BC96516B", "snapshot_id": "SNP-RT-889DAE64", "notification": "triggered", "confidence": 97}	2026-06-17T11:32:36.729039+00:00	2026-06-17T11:32:36.734469+00:00
TASK-RT-53A1BF1B	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-F83A7242", "snapshot_id": "SNP-RT-2DF62FD9", "notification": "triggered", "confidence": 89}	2026-06-17T11:32:55.516634+00:00	2026-06-17T11:32:55.537331+00:00
TASK-0A9D5DF1C6	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C0B71764", "snapshot_id": "SNP-RT-5F94035C", "notification": "triggered", "confidence": 92}	2026-06-17T11:33:06.828325+00:00	2026-06-17T11:33:06.834079+00:00
TASK-RT-C13D4886	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-F712DB9E", "snapshot_id": "SNP-RT-0B74C7D8", "notification": "triggered", "confidence": 94}	2026-06-17T11:33:25.547329+00:00	2026-06-17T11:33:25.562169+00:00
TASK-1A021D3391	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1B63D861", "snapshot_id": "SNP-RT-67E814EF", "notification": "triggered", "confidence": 88}	2026-06-17T11:33:36.934600+00:00	2026-06-17T11:33:36.943492+00:00
TASK-RT-9C9603AD	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-90F85F4D", "snapshot_id": "SNP-RT-0740C0F1", "notification": "triggered", "confidence": 95}	2026-06-17T11:33:55.579793+00:00	2026-06-17T11:33:55.613258+00:00
TASK-8E09BFDAF0	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8CD99719", "snapshot_id": "SNP-RT-E9FDF2A7", "notification": "triggered", "confidence": 98}	2026-06-17T11:34:07.069024+00:00	2026-06-17T11:34:07.074731+00:00
TASK-RT-1F5A7734	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-52986ADA", "snapshot_id": "SNP-RT-466DAC58", "notification": "triggered", "confidence": 91}	2026-06-17T11:34:25.623956+00:00	2026-06-17T11:34:25.640639+00:00
TASK-CFC31D734A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-0E388E10", "snapshot_id": "SNP-RT-38896A15", "notification": "triggered", "confidence": 95}	2026-06-17T11:34:37.239841+00:00	2026-06-17T11:34:37.247604+00:00
TASK-RT-CFC559F1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-DAE56305", "snapshot_id": "SNP-RT-5F58CA16", "notification": "triggered", "confidence": 91}	2026-06-17T11:34:59.269261+00:00	2026-06-17T11:34:59.281482+00:00
TASK-E26FF410EF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A94CA0A1", "snapshot_id": "SNP-RT-0760109A", "notification": "triggered", "confidence": 91}	2026-06-17T11:35:07.350265+00:00	2026-06-17T11:35:07.359048+00:00
TASK-A5135182B5	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BCFCCBE0", "snapshot_id": "SNP-RT-69AE7BBD", "notification": "triggered", "confidence": 90}	2026-06-17T11:35:37.466392+00:00	2026-06-17T11:35:37.475846+00:00
TASK-RT-70088D2A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F7C908CD", "snapshot_id": "SNP-RT-09BAD963", "notification": "triggered", "confidence": 98}	2026-06-17T11:35:56.409036+00:00	2026-06-17T11:35:56.438206+00:00
TASK-67BFFE2E19	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6AA9163B", "snapshot_id": "SNP-RT-9F406360", "notification": "triggered", "confidence": 88}	2026-06-17T11:36:07.606615+00:00	2026-06-17T11:36:07.611346+00:00
TASK-RT-B77D5F9C	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-C5F71D7F", "snapshot_id": "SNP-RT-6BE76F4D", "notification": "triggered", "confidence": 93}	2026-06-17T11:36:26.471352+00:00	2026-06-17T11:36:26.560759+00:00
TASK-58CA437ACB	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1FEBCC6C", "snapshot_id": "SNP-RT-A8379BE2", "notification": "triggered", "confidence": 88}	2026-06-17T11:36:37.723219+00:00	2026-06-17T11:36:37.730538+00:00
TASK-RT-1818F995	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-D21F9CE7", "snapshot_id": "SNP-RT-4B2EEA5B", "notification": "triggered", "confidence": 92}	2026-06-17T11:36:56.590497+00:00	2026-06-17T11:36:56.613834+00:00
TASK-5712E164C4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-925668E7", "snapshot_id": "SNP-RT-E8ADB7BF", "notification": "triggered", "confidence": 90}	2026-06-17T11:37:07.808843+00:00	2026-06-17T11:37:07.817207+00:00
TASK-RT-BC932F80	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-AC22E0AA", "snapshot_id": "SNP-RT-2DE3ADB1", "notification": "triggered", "confidence": 98}	2026-06-17T11:37:26.677292+00:00	2026-06-17T11:37:26.701261+00:00
TASK-4CD864135B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9C1BFE70", "snapshot_id": "SNP-RT-892A07FE", "notification": "triggered", "confidence": 94}	2026-06-17T11:37:37.888704+00:00	2026-06-17T11:37:37.894065+00:00
TASK-RT-C5688D5E	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-BE6D4165", "snapshot_id": "SNP-RT-6B22AA24", "notification": "triggered", "confidence": 94}	2026-06-17T11:37:56.744038+00:00	2026-06-17T11:37:56.754691+00:00
TASK-3E521F5E0B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-20231813", "snapshot_id": "SNP-RT-63306979", "notification": "triggered", "confidence": 92}	2026-06-17T11:38:08.009642+00:00	2026-06-17T11:38:08.014138+00:00
TASK-DD5C1EA7BC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2937B494", "snapshot_id": "SNP-RT-5F90683C", "notification": "triggered", "confidence": 89}	2026-06-17T11:38:38.115758+00:00	2026-06-17T11:38:38.123632+00:00
TASK-RT-33D2C70F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-322597A3", "snapshot_id": "SNP-RT-6BA2F5DF", "notification": "triggered", "confidence": 90}	2026-06-17T11:38:56.983753+00:00	2026-06-17T11:38:57.019639+00:00
TASK-2D8E9F2EE8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9CDA0FE4", "snapshot_id": "SNP-RT-7DA12743", "notification": "triggered", "confidence": 90}	2026-06-17T11:39:08.238881+00:00	2026-06-17T11:39:08.244967+00:00
TASK-RT-228E6BFB	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-669DF586", "snapshot_id": "SNP-RT-6F8E7D97", "notification": "triggered", "confidence": 89}	2026-06-17T11:39:27.027839+00:00	2026-06-17T11:39:27.050801+00:00
TASK-E947FC91EB	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-95117818", "snapshot_id": "SNP-RT-784C7FFD", "notification": "triggered", "confidence": 89}	2026-06-17T11:39:38.340057+00:00	2026-06-17T11:39:38.345341+00:00
TASK-RT-D803B5EE	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-D756BB8B", "snapshot_id": "SNP-RT-5FD8F7B6", "notification": "triggered", "confidence": 99}	2026-06-17T11:39:57.061525+00:00	2026-06-17T11:39:57.097279+00:00
TASK-B67803B82B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-53C72229", "snapshot_id": "SNP-RT-D0B87784", "notification": "triggered", "confidence": 97}	2026-06-17T11:40:08.435862+00:00	2026-06-17T11:40:08.439632+00:00
TASK-RT-E78CA900	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-6CEF0842", "snapshot_id": "SNP-RT-CFE4B675", "notification": "triggered", "confidence": 99}	2026-06-17T11:40:27.109083+00:00	2026-06-17T11:40:27.136671+00:00
TASK-4FC2192CB8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F6C71382", "snapshot_id": "SNP-RT-3CF6B30B", "notification": "triggered", "confidence": 98}	2026-06-17T11:40:38.555120+00:00	2026-06-17T11:40:38.560413+00:00
TASK-RT-EF79DF87	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-8AC7E4CE", "snapshot_id": "SNP-RT-6796F6B1", "notification": "triggered", "confidence": 97}	2026-06-17T11:40:57.149644+00:00	2026-06-17T11:40:57.180904+00:00
TASK-B6B3C54854	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7E8A9DB8", "snapshot_id": "SNP-RT-02B46D8F", "notification": "triggered", "confidence": 88}	2026-06-17T11:41:08.681736+00:00	2026-06-17T11:41:08.686877+00:00
TASK-RT-98EAF3E3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4307A9AB", "snapshot_id": "SNP-RT-1732F109", "notification": "triggered", "confidence": 97}	2026-06-17T11:41:27.274265+00:00	2026-06-17T11:41:27.323101+00:00
TASK-47A48D535E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-73C1462A", "snapshot_id": "SNP-RT-C49B7975", "notification": "triggered", "confidence": 99}	2026-06-17T11:41:38.835868+00:00	2026-06-17T11:41:38.847647+00:00
TASK-RT-3A3F5C8F	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-80A93610", "snapshot_id": "SNP-RT-C6CB91B2", "notification": "triggered", "confidence": 92}	2026-06-17T11:41:57.337732+00:00	2026-06-17T11:41:57.363603+00:00
TASK-7E33C6C8E7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C010D1D7", "snapshot_id": "SNP-RT-89AF4968", "notification": "triggered", "confidence": 88}	2026-06-17T11:42:08.965162+00:00	2026-06-17T11:42:08.971285+00:00
TASK-RT-6B1E19BF	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-79C1C92E", "snapshot_id": "SNP-RT-64D0FBA1", "notification": "triggered", "confidence": 94}	2026-06-17T11:42:27.386172+00:00	2026-06-17T11:42:27.419535+00:00
TASK-17C277DC4C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-027413E3", "snapshot_id": "SNP-RT-F523CA84", "notification": "triggered", "confidence": 97}	2026-06-17T11:42:39.073945+00:00	2026-06-17T11:42:39.080566+00:00
TASK-RT-55BD632A	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-60D3BE49", "snapshot_id": "SNP-RT-B208CEB1", "notification": "triggered", "confidence": 92}	2026-06-17T11:42:57.432739+00:00	2026-06-17T11:42:57.467265+00:00
TASK-FD470DDED5	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-EDBB9C74", "snapshot_id": "SNP-RT-81B50963", "notification": "triggered", "confidence": 89}	2026-06-17T11:43:09.176626+00:00	2026-06-17T11:43:09.181591+00:00
TASK-RT-3C044100	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-B14FE8A3", "snapshot_id": "SNP-RT-3012D5C4", "notification": "triggered", "confidence": 98}	2026-06-17T11:43:27.481921+00:00	2026-06-17T11:43:27.494955+00:00
TASK-C45D81C2AF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C056B0AD", "snapshot_id": "SNP-RT-25BA14C0", "notification": "triggered", "confidence": 97}	2026-06-17T11:43:39.278423+00:00	2026-06-17T11:43:39.281745+00:00
TASK-RT-67251F72	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-556E7387", "snapshot_id": "SNP-RT-73B4BEC2", "notification": "triggered", "confidence": 96}	2026-06-17T11:43:57.506743+00:00	2026-06-17T11:43:57.525290+00:00
TASK-B83C975C00	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-262DB66A", "snapshot_id": "SNP-RT-5524ED6C", "notification": "triggered", "confidence": 92}	2026-06-17T11:44:09.427349+00:00	2026-06-17T11:44:09.433682+00:00
TASK-RT-6FEA7C29	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-38E0A425", "snapshot_id": "SNP-RT-45A196C5", "notification": "triggered", "confidence": 94}	2026-06-17T11:44:27.543834+00:00	2026-06-17T11:44:27.566018+00:00
TASK-17C8B87EFC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-264ABBF5", "snapshot_id": "SNP-RT-F0C17B50", "notification": "triggered", "confidence": 88}	2026-06-17T11:44:39.779079+00:00	2026-06-17T11:44:39.783000+00:00
TASK-RT-5FE7BCF6	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-94A2C0CE", "snapshot_id": "SNP-RT-C3DF744A", "notification": "triggered", "confidence": 89}	2026-06-17T11:44:57.583031+00:00	2026-06-17T11:44:57.607156+00:00
TASK-D274DAFBAD	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2227AE59", "snapshot_id": "SNP-RT-B66C5CAC", "notification": "triggered", "confidence": 91}	2026-06-17T11:45:09.907590+00:00	2026-06-17T11:45:09.912962+00:00
TASK-RT-BD1E233A	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-A1F7A0C6", "snapshot_id": "SNP-RT-AB3DF4A2", "notification": "triggered", "confidence": 92}	2026-06-17T11:45:27.620627+00:00	2026-06-17T11:45:27.644599+00:00
TASK-F0AD9301AC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-126F1D52", "snapshot_id": "SNP-RT-74FF4E4D", "notification": "triggered", "confidence": 88}	2026-06-17T11:45:39.994932+00:00	2026-06-17T11:45:40.005362+00:00
TASK-RT-0DA050C5	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-126B4CF0", "snapshot_id": "SNP-RT-366AE0B4", "notification": "triggered", "confidence": 94}	2026-06-17T11:45:57.655409+00:00	2026-06-17T11:45:57.685226+00:00
TASK-144B5985B8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-91C987CE", "snapshot_id": "SNP-RT-D2DDB334", "notification": "triggered", "confidence": 94}	2026-06-17T11:46:10.110019+00:00	2026-06-17T11:46:10.115330+00:00
TASK-RT-F7AAACE4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-668DAA0B", "snapshot_id": "SNP-RT-22EFC9E1", "notification": "triggered", "confidence": 96}	2026-06-17T11:46:27.702765+00:00	2026-06-17T11:46:27.729251+00:00
TASK-748466EE91	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-DAA0ADEC", "snapshot_id": "SNP-RT-036668F2", "notification": "triggered", "confidence": 97}	2026-06-17T11:46:40.204747+00:00	2026-06-17T11:46:40.210345+00:00
TASK-3ACBD97133	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-99626250", "snapshot_id": "SNP-RT-A8E8F6C3", "notification": "triggered", "confidence": 97}	2026-06-17T11:47:10.302303+00:00	2026-06-17T11:47:10.313616+00:00
TASK-RT-49A2748F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-FF900B5A", "snapshot_id": "SNP-RT-83BF9444", "notification": "triggered", "confidence": 99}	2026-06-17T11:47:12.872613+00:00	2026-06-17T11:47:12.881843+00:00
TASK-6CD0CE3CCE	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-52425C1B", "snapshot_id": "SNP-RT-64DBB2D8", "notification": "triggered", "confidence": 99}	2026-06-17T11:47:40.437673+00:00	2026-06-17T11:47:40.445012+00:00
TASK-RT-244915BD	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1A5BD372", "snapshot_id": "SNP-RT-41F4145A", "notification": "triggered", "confidence": 91}	2026-06-17T11:48:06.558268+00:00	2026-06-17T11:48:06.579918+00:00
TASK-E78378EC05	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6740CC39", "snapshot_id": "SNP-RT-C8119B2E", "notification": "triggered", "confidence": 99}	2026-06-17T11:48:10.574887+00:00	2026-06-17T11:48:10.589017+00:00
TASK-RT-BD1364CC	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-98A0A83F", "snapshot_id": "SNP-RT-7FD2030A", "notification": "triggered", "confidence": 90}	2026-06-17T11:48:36.592713+00:00	2026-06-17T11:48:36.608832+00:00
TASK-03DD37AEF1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BE49213B", "snapshot_id": "SNP-RT-CF1F584D", "notification": "triggered", "confidence": 99}	2026-06-17T11:48:40.829653+00:00	2026-06-17T11:48:40.833956+00:00
TASK-RT-D2D12FEB	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-669EAC64", "snapshot_id": "SNP-RT-9E609FCA", "notification": "triggered", "confidence": 96}	2026-06-17T11:49:06.628843+00:00	2026-06-17T11:49:06.655940+00:00
TASK-B2D120A065	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-106C239D", "snapshot_id": "SNP-RT-F5AA451B", "notification": "triggered", "confidence": 94}	2026-06-17T11:49:10.920619+00:00	2026-06-17T11:49:10.928649+00:00
TASK-RT-EE70A9D1	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-0768B32A", "snapshot_id": "SNP-RT-18C04C6A", "notification": "triggered", "confidence": 88}	2026-06-17T11:49:36.676103+00:00	2026-06-17T11:49:36.705063+00:00
TASK-2590704945	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2ABE3773", "snapshot_id": "SNP-RT-4B4C147E", "notification": "triggered", "confidence": 98}	2026-06-17T11:49:40.994599+00:00	2026-06-17T11:49:40.999999+00:00
TASK-RT-B7D3CFC8	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-AE03A774", "snapshot_id": "SNP-RT-A44F3401", "notification": "triggered", "confidence": 92}	2026-06-17T11:50:06.717511+00:00	2026-06-17T11:50:06.745164+00:00
TASK-462132C88E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-79A62D89", "snapshot_id": "SNP-RT-3869E355", "notification": "triggered", "confidence": 90}	2026-06-17T11:50:11.080399+00:00	2026-06-17T11:50:11.089301+00:00
TASK-RT-1D475EFA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-FA337C07", "snapshot_id": "SNP-RT-0F40B5B9", "notification": "triggered", "confidence": 99}	2026-06-17T11:50:36.753644+00:00	2026-06-17T11:50:36.781671+00:00
TASK-11275000E4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-0B6CBA8E", "snapshot_id": "SNP-RT-3A52F4CA", "notification": "triggered", "confidence": 94}	2026-06-17T11:50:41.183633+00:00	2026-06-17T11:50:41.188126+00:00
TASK-678292BB46	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-287FD0FE", "snapshot_id": "SNP-RT-61EDEB67", "notification": "triggered", "confidence": 97}	2026-06-17T11:51:11.282806+00:00	2026-06-17T11:51:11.287163+00:00
TASK-2CAAC64364	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-523A8E57", "snapshot_id": "SNP-RT-DB544B4D", "notification": "triggered", "confidence": 90}	2026-06-17T11:51:41.389139+00:00	2026-06-17T11:51:41.395002+00:00
TASK-71F520696A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-FA0468B4", "snapshot_id": "SNP-RT-AFA57271", "notification": "triggered", "confidence": 92}	2026-06-17T11:52:11.482361+00:00	2026-06-17T11:52:11.486684+00:00
TASK-DD8CED6325	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8E6FEA13", "snapshot_id": "SNP-RT-FF8C9F78", "notification": "triggered", "confidence": 99}	2026-06-17T11:52:41.579502+00:00	2026-06-17T11:52:41.583010+00:00
TASK-BB55B4C618	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A6C39563", "snapshot_id": "SNP-RT-7309E181", "notification": "triggered", "confidence": 96}	2026-06-17T11:53:11.648889+00:00	2026-06-17T11:53:11.653452+00:00
TASK-07A7B54A00	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-77C48643", "snapshot_id": "SNP-RT-BC655464", "notification": "triggered", "confidence": 89}	2026-06-17T11:53:41.717586+00:00	2026-06-17T11:53:41.720658+00:00
TASK-9F9EF2994B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3F439E86", "snapshot_id": "SNP-RT-2D570AD3", "notification": "triggered", "confidence": 97}	2026-06-17T11:54:11.797421+00:00	2026-06-17T11:54:11.802316+00:00
TASK-RT-461277BD	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-D82FB6D0", "snapshot_id": "SNP-RT-8D0D08DF", "notification": "triggered", "confidence": 94}	2026-06-17T11:51:06.794571+00:00	2026-06-17T11:51:06.822820+00:00
TASK-RT-505FE943	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-FE5F5541", "snapshot_id": "SNP-RT-7C9C2951", "notification": "triggered", "confidence": 96}	2026-06-17T11:51:36.835681+00:00	2026-06-17T11:51:36.857339+00:00
TASK-RT-7353F1A2	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-D34DE4C4", "snapshot_id": "SNP-RT-A0BB4A19", "notification": "triggered", "confidence": 95}	2026-06-17T11:52:06.876027+00:00	2026-06-17T11:52:06.897626+00:00
TASK-RT-0A1670C6	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-8BCE368A", "snapshot_id": "SNP-RT-993C4DA9", "notification": "triggered", "confidence": 92}	2026-06-17T11:52:36.910764+00:00	2026-06-17T11:52:36.930718+00:00
TASK-RT-3ADA0080	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D861E2EC", "snapshot_id": "SNP-RT-63A5AE73", "notification": "triggered", "confidence": 88}	2026-06-17T11:53:06.942709+00:00	2026-06-17T11:53:06.966367+00:00
TASK-RT-48EF3C3E	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-6E8E2AF9", "snapshot_id": "SNP-RT-540DD198", "notification": "triggered", "confidence": 88}	2026-06-17T11:53:36.982359+00:00	2026-06-17T11:53:36.996466+00:00
TASK-RT-D392A7F1	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-504F9EF6", "snapshot_id": "SNP-RT-55342885", "notification": "triggered", "confidence": 90}	2026-06-17T11:54:07.004803+00:00	2026-06-17T11:54:07.022484+00:00
TASK-62B9D8B2D8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-93C7C1D8", "snapshot_id": "SNP-RT-F34FAB60", "notification": "triggered", "confidence": 96}	2026-06-17T11:54:42.009277+00:00	2026-06-17T11:54:42.015780+00:00
TASK-RT-FFADC752	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-50325B06", "snapshot_id": "SNP-RT-51F228C8", "notification": "triggered", "confidence": 89}	2026-06-17T11:55:06.379250+00:00	2026-06-17T11:55:06.396259+00:00
TASK-3A5378DB7E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-97FD0E5D", "snapshot_id": "SNP-RT-A01FB2A1", "notification": "triggered", "confidence": 98}	2026-06-17T11:55:12.115703+00:00	2026-06-17T11:55:12.119628+00:00
TASK-RT-01AC645E	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-D12BBBBE", "snapshot_id": "SNP-RT-3E2288E4", "notification": "triggered", "confidence": 92}	2026-06-17T11:55:36.415659+00:00	2026-06-17T11:55:36.437062+00:00
TASK-43B5051763	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-00D9ED23", "snapshot_id": "SNP-RT-BE8E88AB", "notification": "triggered", "confidence": 98}	2026-06-17T11:55:42.209941+00:00	2026-06-17T11:55:42.213517+00:00
TASK-RT-C47F8394	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-3CF6F2B3", "snapshot_id": "SNP-RT-8D9A789D", "notification": "triggered", "confidence": 96}	2026-06-17T11:56:06.452399+00:00	2026-06-17T11:56:06.479159+00:00
TASK-C88C1CE866	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3054BD93", "snapshot_id": "SNP-RT-64F6A7B6", "notification": "triggered", "confidence": 96}	2026-06-17T11:56:12.329079+00:00	2026-06-17T11:56:12.332051+00:00
TASK-RT-F1DCCA07	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-68167776", "snapshot_id": "SNP-RT-D2375158", "notification": "triggered", "confidence": 98}	2026-06-17T11:56:36.491448+00:00	2026-06-17T11:56:36.523101+00:00
TASK-6A823244B6	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4C9BC8A5", "snapshot_id": "SNP-RT-9BF7AB0D", "notification": "triggered", "confidence": 91}	2026-06-17T11:56:42.415170+00:00	2026-06-17T11:56:42.419223+00:00
TASK-RT-8EE4FBF2	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-6879DCE7", "snapshot_id": "SNP-RT-413EE11C", "notification": "triggered", "confidence": 98}	2026-06-17T11:57:06.540214+00:00	2026-06-17T11:57:06.571616+00:00
TASK-AEE6E86CFC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C8D19DFE", "snapshot_id": "SNP-RT-42DF6B2F", "notification": "triggered", "confidence": 90}	2026-06-17T11:57:12.513913+00:00	2026-06-17T11:57:12.521637+00:00
TASK-RT-47072BAD	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-32E254AA", "snapshot_id": "SNP-RT-1AC59D99", "notification": "triggered", "confidence": 88}	2026-06-17T11:57:36.586823+00:00	2026-06-17T11:57:36.610499+00:00
TASK-0DF92EB59A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-75354B19", "snapshot_id": "SNP-RT-1543DA6B", "notification": "triggered", "confidence": 93}	2026-06-17T11:57:42.632126+00:00	2026-06-17T11:57:42.637592+00:00
TASK-RT-1203B917	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-09453D98", "snapshot_id": "SNP-RT-6403E3EB", "notification": "triggered", "confidence": 95}	2026-06-17T11:58:06.623385+00:00	2026-06-17T11:58:06.657234+00:00
TASK-09A6337464	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-12644B29", "snapshot_id": "SNP-RT-1D62671E", "notification": "triggered", "confidence": 91}	2026-06-17T11:58:12.714207+00:00	2026-06-17T11:58:12.721589+00:00
TASK-RT-A738C95C	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-73569EFF", "snapshot_id": "SNP-RT-6AB8ABD1", "notification": "triggered", "confidence": 91}	2026-06-17T11:58:36.668898+00:00	2026-06-17T11:58:36.687331+00:00
TASK-2120293241	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B3DEC004", "snapshot_id": "SNP-RT-5EB604F9", "notification": "triggered", "confidence": 95}	2026-06-17T11:58:42.843746+00:00	2026-06-17T11:58:42.848825+00:00
TASK-RT-60BDBB50	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-F0EB84F7", "snapshot_id": "SNP-RT-766AFB2E", "notification": "triggered", "confidence": 96}	2026-06-17T11:59:06.695638+00:00	2026-06-17T11:59:06.712218+00:00
TASK-C3A0017CA7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B3F1AA01", "snapshot_id": "SNP-RT-91CEAE8E", "notification": "triggered", "confidence": 96}	2026-06-17T11:59:12.930569+00:00	2026-06-17T11:59:12.936115+00:00
TASK-RT-1EE56C84	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-0E553980", "snapshot_id": "SNP-RT-9BB69C51", "notification": "triggered", "confidence": 97}	2026-06-17T11:59:36.731592+00:00	2026-06-17T11:59:36.753369+00:00
TASK-76474BF344	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9FAF5365", "snapshot_id": "SNP-RT-EC453F34", "notification": "triggered", "confidence": 97}	2026-06-17T11:59:43.047345+00:00	2026-06-17T11:59:43.053271+00:00
TASK-RT-3B753493	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4969E5D5", "snapshot_id": "SNP-RT-67C45F91", "notification": "triggered", "confidence": 98}	2026-06-17T12:00:06.764442+00:00	2026-06-17T12:00:06.779669+00:00
TASK-C981D3ED40	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F537997C", "snapshot_id": "SNP-RT-AA2D2782", "notification": "triggered", "confidence": 92}	2026-06-17T12:00:13.164619+00:00	2026-06-17T12:00:13.173016+00:00
TASK-4D261B8CD5	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7C29A01C", "snapshot_id": "SNP-RT-DE086F0A", "notification": "triggered", "confidence": 89}	2026-06-17T12:00:43.382206+00:00	2026-06-17T12:00:43.389280+00:00
TASK-RT-1A528527	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-7E719E1D", "snapshot_id": "SNP-RT-B7EA83A4", "notification": "triggered", "confidence": 92}	2026-06-17T12:01:07.934697+00:00	2026-06-17T12:01:07.958163+00:00
TASK-A0F59A3F33	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-61DDB512", "snapshot_id": "SNP-RT-CECA373B", "notification": "triggered", "confidence": 90}	2026-06-17T12:01:13.486296+00:00	2026-06-17T12:01:13.489767+00:00
TASK-RT-F70DFB6E	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-A4FF6D99", "snapshot_id": "SNP-RT-B4031EE2", "notification": "triggered", "confidence": 93}	2026-06-17T12:01:37.976111+00:00	2026-06-17T12:01:37.994276+00:00
TASK-1C8F0F813E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2A7D988A", "snapshot_id": "SNP-RT-A4CD787E", "notification": "triggered", "confidence": 95}	2026-06-17T12:01:43.573619+00:00	2026-06-17T12:01:43.579065+00:00
TASK-RT-F813FAFE	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-C4416FC6", "snapshot_id": "SNP-RT-E4E89B8D", "notification": "triggered", "confidence": 96}	2026-06-17T12:02:08.005805+00:00	2026-06-17T12:02:08.040330+00:00
TASK-D2E7BF10B9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-CB7B7406", "snapshot_id": "SNP-RT-7B8B1DCC", "notification": "triggered", "confidence": 99}	2026-06-17T12:02:13.655252+00:00	2026-06-17T12:02:13.659001+00:00
TASK-RT-3C62A605	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-4BD63C4F", "snapshot_id": "SNP-RT-2B6A2078", "notification": "triggered", "confidence": 99}	2026-06-17T12:02:38.059166+00:00	2026-06-17T12:02:38.092381+00:00
TASK-EB7532CE94	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-62821F91", "snapshot_id": "SNP-RT-10418E91", "notification": "triggered", "confidence": 90}	2026-06-17T12:02:43.752080+00:00	2026-06-17T12:02:43.758220+00:00
TASK-RT-71768B5E	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-62BE30DB", "snapshot_id": "SNP-RT-DDB7FBB0", "notification": "triggered", "confidence": 89}	2026-06-17T12:03:08.106877+00:00	2026-06-17T12:03:08.116767+00:00
TASK-10CC0DC920	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1FB78648", "snapshot_id": "SNP-RT-6774E4D2", "notification": "triggered", "confidence": 90}	2026-06-17T12:03:13.840257+00:00	2026-06-17T12:03:13.847926+00:00
TASK-RT-BB93A57A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A43EAFF5", "snapshot_id": "SNP-RT-84EC6357", "notification": "triggered", "confidence": 96}	2026-06-17T12:03:38.139795+00:00	2026-06-17T12:03:38.181174+00:00
TASK-543CBBF7E4	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-05916F02", "snapshot_id": "SNP-RT-80A27F6B", "notification": "triggered", "confidence": 88}	2026-06-17T12:03:43.974192+00:00	2026-06-17T12:03:43.985204+00:00
TASK-RT-3D46BF6D	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-6DF963D3", "snapshot_id": "SNP-RT-9148AA64", "notification": "triggered", "confidence": 93}	2026-06-17T12:04:08.201111+00:00	2026-06-17T12:04:08.217835+00:00
TASK-E13F48F627	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-34486E6B", "snapshot_id": "SNP-RT-4FB7AAA4", "notification": "triggered", "confidence": 99}	2026-06-17T12:04:14.094556+00:00	2026-06-17T12:04:14.101038+00:00
TASK-RT-B69F436A	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-F42681E4", "snapshot_id": "SNP-RT-C71AA4E6", "notification": "triggered", "confidence": 94}	2026-06-17T12:04:38.229489+00:00	2026-06-17T12:04:38.259872+00:00
TASK-760A586782	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-24CC5520", "snapshot_id": "SNP-RT-4F85E516", "notification": "triggered", "confidence": 92}	2026-06-17T12:04:44.208096+00:00	2026-06-17T12:04:44.213149+00:00
TASK-RT-8E733CA8	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-C432BAC4", "snapshot_id": "SNP-RT-5D392791", "notification": "triggered", "confidence": 88}	2026-06-17T12:05:08.273976+00:00	2026-06-17T12:05:08.299454+00:00
TASK-9F762CF9D7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D66C3AD8", "snapshot_id": "SNP-RT-2A83DE7A", "notification": "triggered", "confidence": 90}	2026-06-17T12:05:14.353918+00:00	2026-06-17T12:05:14.359760+00:00
TASK-RT-D6FF86D9	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-EFE0BF04", "snapshot_id": "SNP-RT-D6295644", "notification": "triggered", "confidence": 88}	2026-06-17T12:05:38.312744+00:00	2026-06-17T12:05:38.351296+00:00
TASK-6B436B10B8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8729A921", "snapshot_id": "SNP-RT-BE65F01F", "notification": "triggered", "confidence": 97}	2026-06-17T12:05:44.456113+00:00	2026-06-17T12:05:44.462193+00:00
TASK-4C5207111D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9749D0BE", "snapshot_id": "SNP-RT-6E913647", "notification": "triggered", "confidence": 94}	2026-06-17T12:06:14.590002+00:00	2026-06-17T12:06:14.597805+00:00
TASK-RT-935AFF26	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-5A24C8DB", "snapshot_id": "SNP-RT-DE0B128A", "notification": "triggered", "confidence": 89}	2026-06-17T12:06:23.948142+00:00	2026-06-17T12:06:24.017037+00:00
TASK-9B354C4959	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-243EE828", "snapshot_id": "SNP-RT-7023BABC", "notification": "triggered", "confidence": 88}	2026-06-17T12:06:44.707425+00:00	2026-06-17T12:06:44.712854+00:00
TASK-RT-355D0173	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-8B3863FE", "snapshot_id": "SNP-RT-5E9B0E93", "notification": "triggered", "confidence": 95}	2026-06-17T12:06:54.027454+00:00	2026-06-17T12:06:54.042488+00:00
TASK-BF72882067	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8E482A5F", "snapshot_id": "SNP-RT-40E7E49C", "notification": "triggered", "confidence": 96}	2026-06-17T12:07:14.806024+00:00	2026-06-17T12:07:14.811081+00:00
TASK-RT-000B5037	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-DE6A9A56", "snapshot_id": "SNP-RT-FDE691C4", "notification": "triggered", "confidence": 90}	2026-06-17T12:07:24.061563+00:00	2026-06-17T12:07:24.100045+00:00
TASK-7097B4AEF9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-76DE401E", "snapshot_id": "SNP-RT-3B25D0B5", "notification": "triggered", "confidence": 97}	2026-06-17T12:07:44.914332+00:00	2026-06-17T12:07:44.919657+00:00
TASK-RT-F166A295	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-7B821CF5", "snapshot_id": "SNP-RT-B8038B9C", "notification": "triggered", "confidence": 94}	2026-06-17T12:07:54.108392+00:00	2026-06-17T12:07:54.118079+00:00
TASK-454D570E99	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8796FD30", "snapshot_id": "SNP-RT-B1C19168", "notification": "triggered", "confidence": 96}	2026-06-17T12:08:14.996857+00:00	2026-06-17T12:08:15.001423+00:00
TASK-RT-F11447E1	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-7BBF6AF3", "snapshot_id": "SNP-RT-F0E757FB", "notification": "triggered", "confidence": 93}	2026-06-17T12:08:24.126629+00:00	2026-06-17T12:08:24.152451+00:00
TASK-C127F91255	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C29D2DF8", "snapshot_id": "SNP-RT-6D68CEB3", "notification": "triggered", "confidence": 91}	2026-06-17T12:08:45.086542+00:00	2026-06-17T12:08:45.094246+00:00
TASK-RT-89338E26	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E3D13E99", "snapshot_id": "SNP-RT-6263B431", "notification": "triggered", "confidence": 89}	2026-06-17T12:09:06.543160+00:00	2026-06-17T12:09:06.574699+00:00
TASK-D6F7E28602	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1D88100A", "snapshot_id": "SNP-RT-ADB18917", "notification": "triggered", "confidence": 99}	2026-06-17T12:09:15.199712+00:00	2026-06-17T12:09:15.205817+00:00
TASK-RT-723413C9	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-A3715BA1", "snapshot_id": "SNP-RT-CCC878AA", "notification": "triggered", "confidence": 91}	2026-06-17T12:09:36.593892+00:00	2026-06-17T12:09:36.622634+00:00
TASK-1ED496CD26	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-706066F1", "snapshot_id": "SNP-RT-ABADABAD", "notification": "triggered", "confidence": 92}	2026-06-17T12:09:45.338257+00:00	2026-06-17T12:09:45.342612+00:00
TASK-RT-2C9CC416	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-D84BF75A", "snapshot_id": "SNP-RT-0AEF0771", "notification": "triggered", "confidence": 93}	2026-06-17T12:10:06.639973+00:00	2026-06-17T12:10:06.663667+00:00
TASK-E578CD14D6	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-CE9BC831", "snapshot_id": "SNP-RT-2E015F8F", "notification": "triggered", "confidence": 89}	2026-06-17T12:10:15.417300+00:00	2026-06-17T12:10:15.425863+00:00
TASK-RT-CE102E5D	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-A7AD549E", "snapshot_id": "SNP-RT-05D8BE62", "notification": "triggered", "confidence": 98}	2026-06-17T12:10:36.681752+00:00	2026-06-17T12:10:36.715590+00:00
TASK-A164F0C9C1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A5A077FD", "snapshot_id": "SNP-RT-DEF7CACD", "notification": "triggered", "confidence": 97}	2026-06-17T12:10:45.501477+00:00	2026-06-17T12:10:45.507680+00:00
TASK-SEED-007	CAM-007	animal_intrusion	completed	10	{"source": "seed", "confidence": 90, "event_id": "EVT-007"}	2026-06-17T14:00:00+07:00	2026-06-17T14:00:05+07:00
TASK-68DE265566	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-5ED4AE33", "snapshot_id": "SNP-RT-9A19C47F", "notification": "triggered", "confidence": 91}	2026-06-17T12:11:15.570640+00:00	2026-06-17T12:11:15.575523+00:00
TASK-RT-3B78F637	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-AE0AEFAB", "snapshot_id": "SNP-RT-2598F511", "notification": "triggered", "confidence": 93}	2026-06-17T12:11:35.019189+00:00	2026-06-17T12:11:35.038338+00:00
TASK-EA69B69358	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-44D50ACC", "snapshot_id": "SNP-RT-515AD23A", "notification": "triggered", "confidence": 89}	2026-06-17T12:11:45.653369+00:00	2026-06-17T12:11:45.660353+00:00
TASK-RT-C616E1F7	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-A6308519", "snapshot_id": "SNP-RT-6A2BDD13", "notification": "triggered", "confidence": 89}	2026-06-17T12:12:05.047211+00:00	2026-06-17T12:12:05.070133+00:00
TASK-3103ECCD11	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C07885FD", "snapshot_id": "SNP-RT-F3A7873C", "notification": "triggered", "confidence": 91}	2026-06-17T12:12:15.805566+00:00	2026-06-17T12:12:15.811234+00:00
TASK-RT-B76C3943	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-517512F6", "snapshot_id": "SNP-RT-15046878", "notification": "triggered", "confidence": 90}	2026-06-17T12:12:35.087619+00:00	2026-06-17T12:12:35.103667+00:00
TASK-B759478131	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-68B8EF40", "snapshot_id": "SNP-RT-05E3C747", "notification": "triggered", "confidence": 95}	2026-06-17T12:12:45.921129+00:00	2026-06-17T12:12:45.925815+00:00
TASK-RT-C6F62165	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-2510D1BB", "snapshot_id": "SNP-RT-0BD3F43F", "notification": "triggered", "confidence": 94}	2026-06-17T12:13:05.116211+00:00	2026-06-17T12:13:05.143510+00:00
TASK-D28AD7C382	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-DCEE70A5", "snapshot_id": "SNP-RT-4C148DF3", "notification": "triggered", "confidence": 88}	2026-06-17T12:13:16.049153+00:00	2026-06-17T12:13:16.052884+00:00
TASK-SEED-008	CAM-008	workflow_violation	completed	9	{"source": "seed", "confidence": 91, "event_id": "EVT-008"}	2026-06-17T15:00:00+07:00	2026-06-17T15:00:05+07:00
TASK-SEED-010	CAM-001	restricted_zone_intrusion	queued	7	{"source": "seed", "confidence": 93, "event_id": null}	2026-06-17T17:00:00+07:00	\N
TASK-SEED-011	CAM-002	pig_fever	queued	6	{"source": "seed", "confidence": 94, "event_id": null}	2026-06-17T18:00:00+07:00	\N
TASK-SEED-012	CAM-003	pig_abnormal	queued	5	{"source": "seed", "confidence": 95, "event_id": null}	2026-06-17T19:00:00+07:00	\N
TASK-661E6D9D29	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A72B8A9E", "snapshot_id": "SNP-RT-85650E0D", "notification": "triggered", "confidence": 97}	2026-06-17T12:13:46.157070+00:00	2026-06-17T12:13:46.165730+00:00
TASK-RT-C94A94A7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-CC593150", "snapshot_id": "SNP-RT-9A15179F", "notification": "triggered", "confidence": 96}	2026-06-17T12:13:55.973086+00:00	2026-06-17T12:13:56.000302+00:00
TASK-E16BEEE4E7	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9B4225A4", "snapshot_id": "SNP-RT-AFD51829", "notification": "triggered", "confidence": 93}	2026-06-17T12:14:16.360321+00:00	2026-06-17T12:14:16.368092+00:00
TASK-RT-4EC72A21	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-5350A703", "snapshot_id": "SNP-RT-240125A2", "notification": "triggered", "confidence": 92}	2026-06-17T12:14:44.954221+00:00	2026-06-17T12:14:44.991669+00:00
TASK-49E998584A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BB25B9E5", "snapshot_id": "SNP-RT-48EA74B5", "notification": "triggered", "confidence": 97}	2026-06-17T12:14:46.486456+00:00	2026-06-17T12:14:46.489365+00:00
TASK-RT-AEA38A6C	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-E4B62A01", "snapshot_id": "SNP-RT-193D72E0", "notification": "triggered", "confidence": 92}	2026-06-17T12:15:15.007237+00:00	2026-06-17T12:15:15.043907+00:00
TASK-AEC2DCE7D8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-77610B8A", "snapshot_id": "SNP-RT-D41F84E2", "notification": "triggered", "confidence": 99}	2026-06-17T12:15:16.600979+00:00	2026-06-17T12:15:16.604658+00:00
TASK-RT-A0137723	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-042A8A0D", "snapshot_id": "SNP-RT-5EC0E120", "notification": "triggered", "confidence": 94}	2026-06-17T12:15:45.059646+00:00	2026-06-17T12:15:45.087131+00:00
TASK-F24E0A7B7C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9D5BA740", "snapshot_id": "SNP-RT-BDCF167C", "notification": "triggered", "confidence": 95}	2026-06-17T12:15:46.761261+00:00	2026-06-17T12:15:46.770485+00:00
TASK-RT-1C11EF49	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-FAED45DF", "snapshot_id": "SNP-RT-670D2B6D", "notification": "triggered", "confidence": 97}	2026-06-17T12:16:15.099453+00:00	2026-06-17T12:16:15.123157+00:00
TASK-F9B9354DCF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9A978146", "snapshot_id": "SNP-RT-8B978266", "notification": "triggered", "confidence": 97}	2026-06-17T12:16:16.865654+00:00	2026-06-17T12:16:16.868550+00:00
TASK-E008B4B54D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-40DAA38E", "snapshot_id": "SNP-RT-0E8C884D", "notification": "triggered", "confidence": 93}	2026-06-17T12:16:46.999387+00:00	2026-06-17T12:16:47.013361+00:00
TASK-RT-6120B8EA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-55DA9BE2", "snapshot_id": "SNP-RT-DBC8CD8A", "notification": "triggered", "confidence": 91}	2026-06-17T12:16:50.689044+00:00	2026-06-17T12:16:50.715077+00:00
TASK-5BB1298B27	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A717A77F", "snapshot_id": "SNP-RT-C78C0A26", "notification": "triggered", "confidence": 95}	2026-06-17T12:17:17.245957+00:00	2026-06-17T12:17:17.251381+00:00
TASK-RT-E3C35065	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-0916AD15", "snapshot_id": "SNP-RT-B9F6412B", "notification": "triggered", "confidence": 99}	2026-06-17T12:17:20.759650+00:00	2026-06-17T12:17:20.767391+00:00
TASK-4797842EC8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-75071576", "snapshot_id": "SNP-RT-A14EE8FF", "notification": "triggered", "confidence": 99}	2026-06-17T12:17:47.427314+00:00	2026-06-17T12:17:47.434426+00:00
TASK-RT-AAA0F4E6	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-94B22A2A", "snapshot_id": "SNP-RT-6C749B98", "notification": "triggered", "confidence": 98}	2026-06-17T12:17:50.820797+00:00	2026-06-17T12:17:50.827464+00:00
TASK-04703C2BB1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-39B46F37", "snapshot_id": "SNP-RT-417F3646", "notification": "triggered", "confidence": 96}	2026-06-17T12:18:17.533744+00:00	2026-06-17T12:18:17.537582+00:00
TASK-RT-893D0F62	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-08214CFB", "snapshot_id": "SNP-RT-F10B31AB", "notification": "triggered", "confidence": 95}	2026-06-17T12:18:20.863594+00:00	2026-06-17T12:18:20.897912+00:00
TASK-F167BDBB9F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-38636402", "snapshot_id": "SNP-RT-0F2E261A", "notification": "triggered", "confidence": 98}	2026-06-17T12:18:47.700773+00:00	2026-06-17T12:18:47.710667+00:00
TASK-RT-37A72AAC	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-2F54AE18", "snapshot_id": "SNP-RT-F4C08919", "notification": "triggered", "confidence": 98}	2026-06-17T12:18:50.936081+00:00	2026-06-17T12:18:50.945526+00:00
TASK-5FE8023728	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1FC284BC", "snapshot_id": "SNP-RT-3F469AE8", "notification": "triggered", "confidence": 92}	2026-06-17T12:19:14.775552+00:00	2026-06-17T12:19:14.815062+00:00
TASK-RT-D0203B23	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-87D7DE14", "snapshot_id": "SNP-RT-02E43133", "notification": "triggered", "confidence": 96}	2026-06-17T12:19:36.732209+00:00	2026-06-17T12:19:36.757538+00:00
TASK-E0423E19ED	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E7614EB2", "snapshot_id": "SNP-RT-5A2C50D2", "notification": "triggered", "confidence": 93}	2026-06-17T12:19:45.001129+00:00	2026-06-17T12:19:45.010936+00:00
TASK-RT-EF73A8CF	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-E19C7F8C", "snapshot_id": "SNP-RT-18B8A1C4", "notification": "triggered", "confidence": 89}	2026-06-17T12:20:06.825686+00:00	2026-06-17T12:20:06.855834+00:00
TASK-22FDB91698	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8979345E", "snapshot_id": "SNP-RT-BD789764", "notification": "triggered", "confidence": 92}	2026-06-17T12:20:15.151494+00:00	2026-06-17T12:20:15.158944+00:00
TASK-RT-223B1B1F	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-03BCC394", "snapshot_id": "SNP-RT-2C1DEEB6", "notification": "triggered", "confidence": 90}	2026-06-17T12:20:36.915322+00:00	2026-06-17T12:20:36.941205+00:00
TASK-650CFBF240	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B83DE6C6", "snapshot_id": "SNP-RT-6E34ED11", "notification": "triggered", "confidence": 94}	2026-06-17T12:20:45.278934+00:00	2026-06-17T12:20:45.284812+00:00
TASK-RT-EFB3EB00	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-DCAAA0E8", "snapshot_id": "SNP-RT-ABA0945E", "notification": "triggered", "confidence": 96}	2026-06-17T12:21:06.999201+00:00	2026-06-17T12:21:07.032999+00:00
TASK-838DB40551	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9C41953C", "snapshot_id": "SNP-RT-B23D2A13", "notification": "triggered", "confidence": 90}	2026-06-17T12:21:15.416290+00:00	2026-06-17T12:21:15.437544+00:00
TASK-RT-78B7CD17	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-F33336E4", "snapshot_id": "SNP-RT-4F9BA590", "notification": "triggered", "confidence": 95}	2026-06-17T12:21:37.110993+00:00	2026-06-17T12:21:37.139685+00:00
TASK-57AF279C5D	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-302AF9C6", "snapshot_id": "SNP-RT-562C786F", "notification": "triggered", "confidence": 97}	2026-06-17T12:21:45.601482+00:00	2026-06-17T12:21:45.607506+00:00
TASK-RT-2F60EE66	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-490A521E", "snapshot_id": "SNP-RT-71E8DD15", "notification": "triggered", "confidence": 93}	2026-06-17T12:22:07.205025+00:00	2026-06-17T12:22:07.229044+00:00
TASK-BC76773EE9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3888C83A", "snapshot_id": "SNP-RT-1D967C89", "notification": "triggered", "confidence": 96}	2026-06-17T12:22:15.726999+00:00	2026-06-17T12:22:15.733866+00:00
TASK-764609B39B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-DAD18EA0", "snapshot_id": "SNP-RT-B919AB63", "notification": "triggered", "confidence": 97}	2026-06-17T12:23:16.033615+00:00	2026-06-17T12:23:16.040923+00:00
TASK-00818B2C61	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9357836D", "snapshot_id": "SNP-RT-AF4737CC", "notification": "triggered", "confidence": 93}	2026-06-17T12:24:16.377747+00:00	2026-06-17T12:24:16.385644+00:00
TASK-RT-5C423D46	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-D0240B0E", "snapshot_id": "SNP-RT-246CB529", "notification": "triggered", "confidence": 94}	2026-06-17T12:22:37.288963+00:00	2026-06-17T12:22:37.494726+00:00
TASK-RT-6BB7F5DB	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-AD545480", "snapshot_id": "SNP-RT-3B0E4993", "notification": "triggered", "confidence": 88}	2026-06-17T12:23:37.733163+00:00	2026-06-17T12:23:37.756963+00:00
TASK-RT-48B59829	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-3F574785", "snapshot_id": "SNP-RT-5BD65339", "notification": "triggered", "confidence": 99}	2026-06-17T12:24:37.900571+00:00	2026-06-17T12:24:37.916518+00:00
TASK-66202D1188	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BCB0A674", "snapshot_id": "SNP-RT-FFEC3A8D", "notification": "triggered", "confidence": 90}	2026-06-17T12:22:45.880012+00:00	2026-06-17T12:22:45.887584+00:00
TASK-5F8E541790	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-83008B4F", "snapshot_id": "SNP-RT-C4CED4C3", "notification": "triggered", "confidence": 91}	2026-06-17T12:23:46.214423+00:00	2026-06-17T12:23:46.219931+00:00
TASK-RT-610DAC9B	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-7B15E743", "snapshot_id": "SNP-RT-93CB87E5", "notification": "triggered", "confidence": 91}	2026-06-17T12:23:07.657378+00:00	2026-06-17T12:23:07.681083+00:00
TASK-RT-2E7E75F0	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-47559862", "snapshot_id": "SNP-RT-C55F6D20", "notification": "triggered", "confidence": 93}	2026-06-17T12:24:07.798250+00:00	2026-06-17T12:24:07.821787+00:00
TASK-68A3EB2724	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-127F1B8A", "snapshot_id": "SNP-RT-160894A0", "notification": "triggered", "confidence": 96}	2026-06-17T12:24:46.660568+00:00	2026-06-17T12:24:46.671895+00:00
TASK-RT-288B29A8	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B9ABB01A", "snapshot_id": "SNP-RT-65772B6F", "notification": "triggered", "confidence": 95}	2026-06-17T12:25:12.939090+00:00	2026-06-17T12:25:12.951667+00:00
TASK-F5D8ACF6C3	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D96B147C", "snapshot_id": "SNP-RT-6C2A8C3D", "notification": "triggered", "confidence": 98}	2026-06-17T12:25:16.823778+00:00	2026-06-17T12:25:16.828512+00:00
TASK-A93310DFFC	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1E205229", "snapshot_id": "SNP-RT-ABBEDE36", "notification": "triggered", "confidence": 96}	2026-06-17T12:26:47.175326+00:00	2026-06-17T12:26:47.183583+00:00
TASK-RT-787BB4A1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-4AF32614", "snapshot_id": "SNP-RT-80C867B3", "notification": "triggered", "confidence": 96}	2026-06-17T12:27:01.790916+00:00	2026-06-17T12:27:01.804762+00:00
TASK-DA96D2776E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-0E46F8A8", "snapshot_id": "SNP-RT-1E60CCE1", "notification": "triggered", "confidence": 92}	2026-06-17T12:27:17.394608+00:00	2026-06-17T12:27:17.403104+00:00
TASK-RT-BA136EF2	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-874D74CE", "snapshot_id": "SNP-RT-04E114DE", "notification": "triggered", "confidence": 88}	2026-06-17T12:27:31.873347+00:00	2026-06-17T12:27:31.890043+00:00
TASK-576965C687	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1E1FCD3E", "snapshot_id": "SNP-RT-C295C72C", "notification": "triggered", "confidence": 94}	2026-06-17T12:27:47.545352+00:00	2026-06-17T12:27:47.553124+00:00
TASK-RT-2331C849	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-CE79CE0A", "snapshot_id": "SNP-RT-E2D924F9", "notification": "triggered", "confidence": 94}	2026-06-17T12:28:01.953108+00:00	2026-06-17T12:28:01.975823+00:00
TASK-768C0C5E9A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-C95A8A0E", "snapshot_id": "SNP-RT-AA3F1CFA", "notification": "triggered", "confidence": 89}	2026-06-17T12:28:17.681474+00:00	2026-06-17T12:28:17.688481+00:00
TASK-RT-7BCCF284	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-7534788E", "snapshot_id": "SNP-RT-D4AB3A26", "notification": "triggered", "confidence": 89}	2026-06-17T12:28:32.035163+00:00	2026-06-17T12:28:32.064782+00:00
TASK-A5D479433B	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1747DCB2", "snapshot_id": "SNP-RT-CD24C6D4", "notification": "triggered", "confidence": 95}	2026-06-17T12:28:47.838788+00:00	2026-06-17T12:28:47.845112+00:00
TASK-RT-A0800A67	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-920B3643", "snapshot_id": "SNP-RT-B01A5DDB", "notification": "triggered", "confidence": 96}	2026-06-17T12:29:02.119109+00:00	2026-06-17T12:29:02.135045+00:00
TASK-81AF32E84F	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-52277007", "snapshot_id": "SNP-RT-F9DBEE35", "notification": "triggered", "confidence": 88}	2026-06-17T12:29:48.131602+00:00	2026-06-17T12:29:48.139037+00:00
TASK-RT-8854EDA1	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1F91C61C", "snapshot_id": "SNP-RT-FF5F1EF4", "notification": "triggered", "confidence": 98}	2026-06-17T12:30:10.845214+00:00	2026-06-17T12:30:10.854192+00:00
TASK-713E4072BA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-040AC757", "snapshot_id": "SNP-RT-8F578E54", "notification": "triggered", "confidence": 95}	2026-06-17T12:30:18.314625+00:00	2026-06-17T12:30:18.319308+00:00
TASK-RT-1F505D62	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-DC672173", "snapshot_id": "SNP-RT-F321E0EA", "notification": "triggered", "confidence": 90}	2026-06-17T12:30:40.908548+00:00	2026-06-17T12:30:40.921408+00:00
TASK-DC67CD8EB5	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E3F74136", "snapshot_id": "SNP-RT-8CE7777E", "notification": "triggered", "confidence": 96}	2026-06-17T12:30:48.449522+00:00	2026-06-17T12:30:48.453409+00:00
TASK-RT-F08BB091	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-EE1C72FC", "snapshot_id": "SNP-RT-E8D18471", "notification": "triggered", "confidence": 96}	2026-06-17T12:31:10.984144+00:00	2026-06-17T12:31:11.000101+00:00
TASK-23D5A34786	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-465C5378", "snapshot_id": "SNP-RT-8B1182F2", "notification": "triggered", "confidence": 96}	2026-06-17T12:31:18.580576+00:00	2026-06-17T12:31:18.588290+00:00
TASK-RT-F0976D26	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-0DC24FD7", "snapshot_id": "SNP-RT-2DE616B5", "notification": "triggered", "confidence": 96}	2026-06-17T12:31:41.068414+00:00	2026-06-17T12:31:41.093798+00:00
TASK-703E7A0AFF	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-06BAB461", "snapshot_id": "SNP-RT-DA095CBB", "notification": "triggered", "confidence": 96}	2026-06-17T12:31:48.746656+00:00	2026-06-17T12:31:48.757559+00:00
TASK-RT-84A2694A	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-B011B8CD", "snapshot_id": "SNP-RT-BF3A7C4C", "notification": "triggered", "confidence": 93}	2026-06-17T12:32:11.137164+00:00	2026-06-17T12:32:11.152568+00:00
TASK-17662BEBAA	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-BB297A1E", "snapshot_id": "SNP-RT-198E0B82", "notification": "triggered", "confidence": 90}	2026-06-17T12:32:18.901331+00:00	2026-06-17T12:32:18.906915+00:00
TASK-RT-F5302C6E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1DB45716", "snapshot_id": "SNP-RT-51528A55", "notification": "triggered", "confidence": 99}	2026-06-17T12:32:41.214583+00:00	2026-06-17T12:32:41.229852+00:00
TASK-0080693F24	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-6DBF0A6F", "snapshot_id": "SNP-RT-26915CBD", "notification": "triggered", "confidence": 92}	2026-06-17T12:32:49.036147+00:00	2026-06-17T12:32:49.040932+00:00
TASK-RT-7BFE9769	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-4B10B881", "snapshot_id": "SNP-RT-715949C3", "notification": "triggered", "confidence": 99}	2026-06-17T12:33:11.289133+00:00	2026-06-17T12:33:11.302167+00:00
TASK-E221CC2E69	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-80FD7557", "snapshot_id": "SNP-RT-9B70ED5A", "notification": "triggered", "confidence": 96}	2026-06-17T12:33:19.160045+00:00	2026-06-17T12:33:19.167306+00:00
TASK-C2BCCDB9CE	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-1C90AA58", "snapshot_id": "SNP-RT-BBC987B8", "notification": "triggered", "confidence": 98}	2026-06-17T12:33:49.299258+00:00	2026-06-17T12:33:49.307830+00:00
TASK-RT-85A37A93	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-952C9BAB", "snapshot_id": "SNP-RT-E276C81F", "notification": "triggered", "confidence": 98}	2026-06-17T12:34:11.420236+00:00	2026-06-17T12:34:11.430761+00:00
TASK-RT-0749546A	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-06B42C62", "snapshot_id": "SNP-RT-2B5A8E23", "notification": "triggered", "confidence": 88}	2026-06-17T12:33:41.345778+00:00	2026-06-17T12:33:41.359564+00:00
TASK-2CA397F905	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F90EE8A7", "snapshot_id": "SNP-RT-B641868B", "notification": "triggered", "confidence": 99}	2026-06-17T12:34:19.459449+00:00	2026-06-17T12:34:19.467035+00:00
TASK-RT-96BE581A	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-50800B4C", "snapshot_id": "SNP-RT-F5CC7600", "notification": "triggered", "confidence": 89}	2026-06-17T12:34:41.497893+00:00	2026-06-17T12:34:41.519101+00:00
TASK-ED85F54E50	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F9E18578", "snapshot_id": "SNP-RT-0318AE89", "notification": "triggered", "confidence": 92}	2026-06-17T12:34:49.596824+00:00	2026-06-17T12:34:49.602705+00:00
TASK-RT-105C3D6E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-07E9DDB7", "snapshot_id": "SNP-RT-248EBFAB", "notification": "triggered", "confidence": 97}	2026-06-17T12:35:11.564083+00:00	2026-06-17T12:35:11.576786+00:00
TASK-3E4E9D8087	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-8A91E029", "snapshot_id": "SNP-RT-F6C1B06B", "notification": "triggered", "confidence": 98}	2026-06-17T12:35:19.767229+00:00	2026-06-17T12:35:19.780759+00:00
TASK-CE9685B498	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-300E78E2", "snapshot_id": "SNP-RT-4B898F6F", "notification": "triggered", "confidence": 94}	2026-06-17T12:36:19.983979+00:00	2026-06-17T12:36:19.994333+00:00
TASK-RT-2C974F37	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-B9365C23", "snapshot_id": "SNP-RT-91876A2E", "notification": "triggered", "confidence": 92}	2026-06-17T12:36:34.275776+00:00	2026-06-17T12:36:34.306283+00:00
TASK-F6DE67EB32	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-51561BA6", "snapshot_id": "SNP-RT-8EC37D73", "notification": "triggered", "confidence": 95}	2026-06-17T12:36:50.133795+00:00	2026-06-17T12:36:50.140168+00:00
TASK-RT-406F06B5	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-2F8E7668", "snapshot_id": "SNP-RT-07A7F427", "notification": "triggered", "confidence": 96}	2026-06-17T12:37:04.365141+00:00	2026-06-17T12:37:04.400230+00:00
TASK-24496E2062	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2EA3206A", "snapshot_id": "SNP-RT-0F554227", "notification": "triggered", "confidence": 89}	2026-06-17T12:37:20.290799+00:00	2026-06-17T12:37:20.303016+00:00
TASK-RT-26AF4E21	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-0A9227A3", "snapshot_id": "SNP-RT-BC5538D3", "notification": "triggered", "confidence": 95}	2026-06-17T12:37:34.458723+00:00	2026-06-17T12:37:34.485152+00:00
TASK-A5028A92F9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-A8071FB6", "snapshot_id": "SNP-RT-78987922", "notification": "triggered", "confidence": 88}	2026-06-17T12:37:50.474994+00:00	2026-06-17T12:37:50.479419+00:00
TASK-RT-1991EF94	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-A7A24170", "snapshot_id": "SNP-RT-B44D2725", "notification": "triggered", "confidence": 96}	2026-06-17T12:38:04.542473+00:00	2026-06-17T12:38:04.577998+00:00
TASK-200A21CE4E	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-D7D28C77", "snapshot_id": "SNP-RT-252C3D4D", "notification": "triggered", "confidence": 89}	2026-06-17T12:38:20.630169+00:00	2026-06-17T12:38:20.638298+00:00
TASK-RT-6EAB69C4	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-0F04704E", "snapshot_id": "SNP-RT-CD12D571", "notification": "triggered", "confidence": 90}	2026-06-17T12:38:34.624065+00:00	2026-06-17T12:38:34.643925+00:00
TASK-DD811CB648	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-9AA0D6C5", "snapshot_id": "SNP-RT-5DF42562", "notification": "triggered", "confidence": 96}	2026-06-17T12:38:50.772296+00:00	2026-06-17T12:38:50.778386+00:00
TASK-RT-045DBF7C	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-F765A692", "snapshot_id": "SNP-RT-E94920F2", "notification": "triggered", "confidence": 90}	2026-06-17T12:39:04.690254+00:00	2026-06-17T12:39:04.716179+00:00
TASK-FD9A08EADD	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-24285AB9", "snapshot_id": "SNP-RT-DF7E13E1", "notification": "triggered", "confidence": 99}	2026-06-17T12:39:20.963505+00:00	2026-06-17T12:39:20.972681+00:00
TASK-RT-8CB70F1C	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-4805F23E", "snapshot_id": "SNP-RT-479B8A2E", "notification": "triggered", "confidence": 89}	2026-06-17T12:39:34.774657+00:00	2026-06-17T12:39:34.804034+00:00
TASK-74E1AE3998	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-E13E7CB9", "snapshot_id": "SNP-RT-8C0A141F", "notification": "triggered", "confidence": 91}	2026-06-17T12:39:51.149821+00:00	2026-06-17T12:39:51.155885+00:00
TASK-RT-7980DB36	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-D77F7CC8", "snapshot_id": "SNP-RT-218ABC82", "notification": "triggered", "confidence": 90}	2026-06-17T12:40:04.865532+00:00	2026-06-17T12:40:04.887917+00:00
TASK-CB7081A358	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-02801074", "snapshot_id": "SNP-RT-6D2981AD", "notification": "triggered", "confidence": 95}	2026-06-17T12:40:21.326776+00:00	2026-06-17T12:40:21.334186+00:00
TASK-RT-3591CCD9	CAM-005	camera_offline	completed	10	{"event_id": "EVT-RT-AAE0629F", "snapshot_id": "SNP-RT-18952AC7", "notification": "triggered", "confidence": 91}	2026-06-17T12:40:34.947753+00:00	2026-06-17T12:40:34.973721+00:00
TASK-4081ADFB35	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-2E09042E", "snapshot_id": "SNP-RT-0580D3C2", "notification": "triggered", "confidence": 89}	2026-06-17T12:40:51.496026+00:00	2026-06-17T12:40:51.507140+00:00
TASK-RT-662F0C1F	CAM-008	vehicle_disinfection	completed	7	{"event_id": "EVT-RT-58CD44C6", "snapshot_id": "SNP-RT-16F09FD7", "notification": "triggered", "confidence": 91}	2026-06-17T12:41:05.026622+00:00	2026-06-17T12:41:05.055834+00:00
TASK-594BE019BE	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-CBB3FD58", "snapshot_id": "SNP-RT-35328ED6", "notification": "triggered", "confidence": 97}	2026-06-17T12:41:21.668598+00:00	2026-06-17T12:41:21.678034+00:00
TASK-RT-E68CB28A	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-649921F1", "snapshot_id": "SNP-RT-C9355CE7", "notification": "triggered", "confidence": 94}	2026-06-17T12:41:35.116194+00:00	2026-06-17T12:41:35.146598+00:00
TASK-02A98BB514	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-20F6A442", "snapshot_id": "SNP-RT-AFD8A312", "notification": "triggered", "confidence": 88}	2026-06-17T12:41:51.859748+00:00	2026-06-17T12:41:51.869242+00:00
TASK-RT-7748E39E	CAM-002	pig_fever	completed	8	{"event_id": "EVT-RT-78D7F067", "snapshot_id": "SNP-RT-4FFF0942", "notification": "triggered", "confidence": 93}	2026-06-17T12:42:05.215138+00:00	2026-06-17T12:42:05.238121+00:00
TASK-BAE0F2DBF9	CAM-001	restricted_zone_intrusion	completed	9	{"event_id": "EVT-RT-00E443C2", "snapshot_id": "SNP-RT-C8FA4E04", "notification": "triggered", "confidence": 96}	2026-06-17T12:42:22.049637+00:00	2026-06-17T12:42:22.056842+00:00
TASK-RT-C4E162C8	CAM-004	pig_abnormal	completed	10	{"event_id": "EVT-RT-44E2C2AE", "snapshot_id": "SNP-RT-8AE51310", "notification": "triggered", "confidence": 93}	2026-06-17T12:42:35.298000+00:00	2026-06-17T12:42:35.325725+00:00
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.alembic_version (version_num) FROM stdin;
0018_workflow_engine_v31
\.


--
-- Data for Name: alert_categories; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.alert_categories (code, label, severity) FROM stdin;
improper_clothing	Người không đúng trang phục	warning
restricted_zone_intrusion	Người và động vật xâm nhập vùng cấm	danger
pig_fever	Heo sốt bất thường	danger
pig_abnormal	Heo nằm bất động kéo dài	critical
vehicle_disinfection	Xe chưa qua khử trùng	warning
camera_offline	Camera mất kết nối	critical
animal_intrusion	Động vật xâm nhập vùng cấm	danger
workflow_violation	Vi phạm quy trình ATSH	critical
\.


--
-- Data for Name: animal_intrusion_policies; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.animal_intrusion_policies (id, object_type, allowed_zones, restricted_zones, severity, enabled) FROM stdin;
AIP-DOG	dog	["parking_zone", "reception_zone", "pig_loading_zone"]	["gestation_barn", "farrowing_barn", "weaning_barn", "nursery_barn"]	critical	t
AIP-CAT	cat	["parking_zone", "reception_zone", "guard_house"]	["gestation_barn", "farrowing_barn", "weaning_barn", "boar_barn", "nursery_barn"]	high	t
AIP-RAT	rat	["parking_zone", "reception_zone"]	["vet_medicine_storage", "feed_storage", "medicine_warehouse", "feed_warehouse"]	critical	t
AIP-BIRD	bird	["parking_zone", "reception_zone", "guard_house"]	["feed_storage", "feed_warehouse"]	warning	t
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.audit_logs (id, user_id, action, resource_type, resource_id, metadata_json, created_at) FROM stdin;
AUD-B50FE33F6892	USR-ADMIN	login	auth	USR-ADMIN	{"email": "admin@ams.local"}	2026-06-17T10:05:20.406149+00:00
AUD-35EC1C92C158	SYSTEM	ai_task_completed	ai_task	TASK-A6573A79DA	{"event_id": "EVT-RT-BFC14B09", "snapshot_id": "SNP-RT-E18F89D8"}	2026-06-17T10:05:20.428588+00:00
AUD-BCE6E4A2D62A	USR-ADMIN	logout	auth	USR-ADMIN	{"jti": "2f871b9285aa4ca2b9cc10d54b6d3ec0"}	2026-06-17T10:05:20.452518+00:00
AUD-EA61A098287C	SYSTEM	ai_task_completed	ai_task	TASK-RT-1041656A	{"event_id": "EVT-RT-ABAB9E7D", "snapshot_id": "SNP-RT-0DB16962"}	2026-06-17T10:05:36.019498+00:00
AUD-51C57761619B	SYSTEM	ai_task_completed	ai_task	TASK-RT-F59EC88E	{"event_id": "EVT-RT-6BB404E1", "snapshot_id": "SNP-RT-50F07727"}	2026-06-17T10:06:39.554243+00:00
AUD-9185F8F8DDF7	SYSTEM	ai_task_completed	ai_task	TASK-RT-899057AD	{"event_id": "EVT-RT-9599DF0C", "snapshot_id": "SNP-RT-833A090A"}	2026-06-17T10:07:09.598236+00:00
AUD-B076FA4C48A6	SYSTEM	ai_task_completed	ai_task	TASK-RT-0EE844EF	{"event_id": "EVT-RT-E338BA34", "snapshot_id": "SNP-RT-677B91EC"}	2026-06-17T10:07:39.629075+00:00
AUD-0852DEDA2E2C	SYSTEM	ai_task_completed	ai_task	TASK-RT-0E51FA97	{"event_id": "EVT-RT-70D6A36E", "snapshot_id": "SNP-RT-C4A7AF0F"}	2026-06-17T10:08:09.673726+00:00
AUD-8A0C4040B97E	SYSTEM	ai_task_completed	ai_task	TASK-RT-CB24EF83	{"event_id": "EVT-RT-A5AD8924", "snapshot_id": "SNP-RT-1B431BAA"}	2026-06-17T10:08:39.708968+00:00
AUD-2FA091625F6A	SYSTEM	ai_task_completed	ai_task	TASK-RT-7DCC3DB4	{"event_id": "EVT-RT-9277B021", "snapshot_id": "SNP-RT-39E7F534"}	2026-06-17T10:09:09.743970+00:00
AUD-823877903E8C	SYSTEM	ai_task_completed	ai_task	TASK-RT-2D4AC891	{"event_id": "EVT-RT-9A030D8C", "snapshot_id": "SNP-RT-39BFF036"}	2026-06-17T10:09:39.789530+00:00
AUD-D1F3026C0F1A	SYSTEM	ai_task_completed	ai_task	TASK-RT-9EEAAF89	{"event_id": "EVT-RT-34FB34CF", "snapshot_id": "SNP-RT-35CAFBC6"}	2026-06-17T10:10:09.828180+00:00
AUD-C0D102A7632E	SYSTEM	ai_task_completed	ai_task	TASK-RT-08E282E6	{"event_id": "EVT-RT-C46862AA", "snapshot_id": "SNP-RT-1487B010"}	2026-06-17T10:10:39.858666+00:00
AUD-0F1FC634194E	SYSTEM	ai_task_completed	ai_task	TASK-RT-21EF091B	{"event_id": "EVT-RT-927CC36B", "snapshot_id": "SNP-RT-F6F3D5D2"}	2026-06-17T10:11:09.881767+00:00
AUD-1E3B3DBB4346	SYSTEM	ai_task_completed	ai_task	TASK-RT-EC86A85C	{"event_id": "EVT-RT-876895A2", "snapshot_id": "SNP-RT-7F2A5C87"}	2026-06-17T10:11:39.906788+00:00
AUD-8547B1921D11	SYSTEM	ai_task_completed	ai_task	TASK-RT-A45F448B	{"event_id": "EVT-RT-2D922793", "snapshot_id": "SNP-RT-B7F0A587"}	2026-06-17T10:12:09.937903+00:00
AUD-A7127CBB7E01	SYSTEM	ai_task_completed	ai_task	TASK-RT-0F5EB290	{"event_id": "EVT-RT-C423F422", "snapshot_id": "SNP-RT-FB84D30A"}	2026-06-17T10:12:39.955307+00:00
AUD-5435DFC3F75D	USR-ADMIN	login	auth	USR-ADMIN	{"email": "admin@ams.local"}	2026-06-17T10:13:30.109686+00:00
AUD-B0B41EF1E883	SYSTEM	ai_task_completed	ai_task	TASK-E9EDF1D13C	{"event_id": "EVT-RT-DE295378", "snapshot_id": "SNP-RT-22114E02"}	2026-06-17T10:13:30.137221+00:00
AUD-E1D28634B7BE	SYSTEM	ai_task_completed	ai_task	TASK-RT-2502BDA3	{"event_id": "EVT-RT-02F7DF6A", "snapshot_id": "SNP-RT-1A7DB589"}	2026-06-17T10:13:46.592473+00:00
AUD-67057D274784	SYSTEM	ai_task_completed	ai_task	TASK-E12DB6E3C8	{"event_id": "EVT-RT-E3500358", "snapshot_id": "SNP-RT-01668253"}	2026-06-17T10:39:51.622729+00:00
AUD-B1D1D3608A61	SYSTEM	ai_task_completed	ai_task	TASK-BD07C36E20	{"event_id": "EVT-RT-08DE7C83", "snapshot_id": "SNP-RT-4756FC06"}	2026-06-17T10:40:02.624785+00:00
AUD-15F26320C953	SYSTEM	ai_task_completed	ai_task	TASK-207C21B740	{"event_id": "EVT-RT-17B29287", "snapshot_id": "SNP-RT-B9953C15"}	2026-06-17T10:40:21.731776+00:00
AUD-1C2C3C8B193A	SYSTEM	ai_task_completed	ai_task	TASK-820FC47E53	{"event_id": "EVT-RT-81276D8F", "snapshot_id": "SNP-RT-B7D73998"}	2026-06-17T10:40:51.826204+00:00
AUD-E844113BCE8D	SYSTEM	ai_task_completed	ai_task	TASK-9516EAB9D0	{"event_id": "EVT-RT-CEC94A75", "snapshot_id": "SNP-RT-4488BA09"}	2026-06-17T10:41:22.073321+00:00
AUD-18D073E7D115	SYSTEM	ai_task_completed	ai_task	TASK-D4498DD574	{"event_id": "EVT-RT-3D1B30D7", "snapshot_id": "SNP-RT-0F14A9B3"}	2026-06-17T10:41:52.335628+00:00
AUD-426412D36089	SYSTEM	ai_task_completed	ai_task	TASK-C393999C2C	{"event_id": "EVT-RT-BAE6E1D7", "snapshot_id": "SNP-RT-AEDC5B77"}	2026-06-17T10:42:22.457017+00:00
AUD-3137B8AB26F8	SYSTEM	ai_task_completed	ai_task	TASK-77218524C2	{"event_id": "EVT-RT-84A7C1CC", "snapshot_id": "SNP-RT-FB3141A1"}	2026-06-17T10:42:52.567499+00:00
AUD-C69E437D9768	SYSTEM	ai_task_completed	ai_task	TASK-09F24396AB	{"event_id": "EVT-RT-8E95A8E7", "snapshot_id": "SNP-RT-BEBF895E"}	2026-06-17T10:43:22.668512+00:00
AUD-959387DEA0B7	SYSTEM	ai_task_completed	ai_task	TASK-9341FBCCF9	{"event_id": "EVT-RT-9BD213BC", "snapshot_id": "SNP-RT-E191AF81"}	2026-06-17T10:43:52.770435+00:00
AUD-E1CAE32977E8	SYSTEM	ai_task_completed	ai_task	TASK-98B47A3F46	{"event_id": "EVT-RT-6D08308D", "snapshot_id": "SNP-RT-9126DA26"}	2026-06-17T10:44:22.837517+00:00
AUD-C897AD6D920C	SYSTEM	ai_task_completed	ai_task	TASK-91BEE9064E	{"event_id": "EVT-RT-D466ABAC", "snapshot_id": "SNP-RT-48B03081"}	2026-06-17T10:44:52.953996+00:00
AUD-CF05524E19BA	SYSTEM	ai_task_completed	ai_task	TASK-6C3A429B55	{"event_id": "EVT-RT-AC0705AD", "snapshot_id": "SNP-RT-CB8F77E0"}	2026-06-17T10:45:23.054919+00:00
AUD-88977B6907B6	SYSTEM	ai_task_completed	ai_task	TASK-D6632352AA	{"event_id": "EVT-RT-915DA336", "snapshot_id": "SNP-RT-CC6A91DE"}	2026-06-17T10:45:53.161432+00:00
AUD-E4F5711B8181	SYSTEM	ai_task_completed	ai_task	TASK-936BE1AED3	{"event_id": "EVT-RT-6B65B8F0", "snapshot_id": "SNP-RT-4EB86ACB"}	2026-06-17T10:46:23.256558+00:00
AUD-SEED-001	USR-ADMIN	login	system	SEED-001	{"source": "seed"}	2026-06-17T12:35:21.742709+00:00
AUD-SEED-002	USR-ADMIN	logout	system	SEED-002	{"source": "seed"}	2026-06-17T12:35:21.742709+00:00
AUD-SEED-003	USR-ADMIN	create_camera	system	SEED-003	{"source": "seed"}	2026-06-17T12:35:21.742709+00:00
AUD-SEED-004	USR-ADMIN	update_notification_rule	system	SEED-004	{"source": "seed"}	2026-06-17T12:35:21.742709+00:00
AUD-88C9637E28D6	SYSTEM	ai_task_completed	ai_task	TASK-08B63B76E0	{"event_id": "EVT-RT-BD626578", "snapshot_id": "SNP-RT-9309CD64"}	2026-06-17T10:46:53.362964+00:00
AUD-F0E18675CEF1	SYSTEM	ai_task_completed	ai_task	TASK-B5B2BAA16F	{"event_id": "EVT-RT-BE27BDC6", "snapshot_id": "SNP-RT-0D3DE2B0"}	2026-06-17T10:47:23.474122+00:00
AUD-61FFBF8EA3D1	SYSTEM	ai_task_completed	ai_task	TASK-DFDB43D4EA	{"event_id": "EVT-RT-73006EA4", "snapshot_id": "SNP-RT-7B782F3D"}	2026-06-17T10:47:53.576170+00:00
AUD-D403C6A5DC27	SYSTEM	ai_task_completed	ai_task	TASK-5C1594D82C	{"event_id": "EVT-RT-A480BC66", "snapshot_id": "SNP-RT-51D2EB19"}	2026-06-17T10:48:23.664913+00:00
AUD-F5FE6C5B9583	SYSTEM	ai_task_completed	ai_task	TASK-D48FE37DA7	{"event_id": "EVT-RT-6A2EEA15", "snapshot_id": "SNP-RT-5513A9A8"}	2026-06-17T10:48:53.772275+00:00
AUD-6820597B2F58	SYSTEM	ai_task_completed	ai_task	TASK-7CA7C54C38	{"event_id": "EVT-RT-7A471A36", "snapshot_id": "SNP-RT-2701EAEE"}	2026-06-17T10:49:23.893807+00:00
AUD-5A1AC43C0E80	SYSTEM	ai_task_completed	ai_task	TASK-04DD1E403D	{"event_id": "EVT-RT-A578B0E9", "snapshot_id": "SNP-RT-F9D2AA67"}	2026-06-17T10:49:53.996449+00:00
AUD-F58AFC7C9FEC	SYSTEM	ai_task_completed	ai_task	TASK-F97EB49B88	{"event_id": "EVT-RT-9FF2F5FA", "snapshot_id": "SNP-RT-747E79C9"}	2026-06-17T10:50:24.085128+00:00
AUD-F6340234464F	SYSTEM	ai_task_completed	ai_task	TASK-26DC58A60F	{"event_id": "EVT-RT-D1863B4B", "snapshot_id": "SNP-RT-2582CCFD"}	2026-06-17T10:50:54.183333+00:00
AUD-8B20307600B6	SYSTEM	ai_task_completed	ai_task	TASK-317E4AD58E	{"event_id": "EVT-RT-F0842F88", "snapshot_id": "SNP-RT-DC9FF292"}	2026-06-17T10:51:24.299882+00:00
AUD-20005C495559	SYSTEM	ai_task_completed	ai_task	TASK-5B87C1C8B1	{"event_id": "EVT-RT-DF66D38B", "snapshot_id": "SNP-RT-92486101"}	2026-06-17T10:51:54.416811+00:00
AUD-9F25D464E1DF	SYSTEM	ai_task_completed	ai_task	TASK-835B9F7C22	{"event_id": "EVT-RT-7C31CBAF", "snapshot_id": "SNP-RT-09A4C2B0"}	2026-06-17T10:52:24.603162+00:00
AUD-16C8451348F3	SYSTEM	ai_task_completed	ai_task	TASK-EA10D36956	{"event_id": "EVT-RT-5BCE2E00", "snapshot_id": "SNP-RT-E03AD713"}	2026-06-17T10:52:54.711719+00:00
AUD-96D788121BFA	SYSTEM	ai_task_completed	ai_task	TASK-780076B84E	{"event_id": "EVT-RT-D193DAD9", "snapshot_id": "SNP-RT-3574621F"}	2026-06-17T10:53:24.808129+00:00
AUD-888321C91581	SYSTEM	ai_task_completed	ai_task	TASK-63E7A2B3DF	{"event_id": "EVT-RT-B8FA3700", "snapshot_id": "SNP-RT-E27ED637"}	2026-06-17T10:53:54.919348+00:00
AUD-F57E492FC243	SYSTEM	ai_task_completed	ai_task	TASK-4515C540F4	{"event_id": "EVT-RT-21536871", "snapshot_id": "SNP-RT-A58976C4"}	2026-06-17T10:54:25.014074+00:00
AUD-02E910F07482	SYSTEM	ai_task_completed	ai_task	TASK-AA1991BBE1	{"event_id": "EVT-RT-FA3F75F4", "snapshot_id": "SNP-RT-B6E85CBE"}	2026-06-17T10:54:55.132890+00:00
AUD-F21481F4A0FA	SYSTEM	ai_task_completed	ai_task	TASK-D077839DC1	{"event_id": "EVT-RT-CC39D3BF", "snapshot_id": "SNP-RT-C8FA1717"}	2026-06-17T10:55:25.244561+00:00
AUD-B691B511D6E3	SYSTEM	ai_task_completed	ai_task	TASK-25620BC7C9	{"event_id": "EVT-RT-8FC08AB1", "snapshot_id": "SNP-RT-D7AC0941"}	2026-06-17T10:55:55.324724+00:00
AUD-E39D8580A087	SYSTEM	ai_task_completed	ai_task	TASK-C7CD3337CC	{"event_id": "EVT-RT-6496304B", "snapshot_id": "SNP-RT-D6FB9A5A"}	2026-06-17T10:56:25.450177+00:00
AUD-066C2FAE8BDD	SYSTEM	ai_task_completed	ai_task	TASK-29218EF9C4	{"event_id": "EVT-RT-58C22B56", "snapshot_id": "SNP-RT-D6CB3AEC"}	2026-06-17T10:56:55.550908+00:00
AUD-E4BB01EB9DC9	SYSTEM	ai_task_completed	ai_task	TASK-82E23A4ED7	{"event_id": "EVT-RT-8C2CD6F7", "snapshot_id": "SNP-RT-32C3A2C8"}	2026-06-17T10:57:25.655425+00:00
AUD-BFD37E958929	SYSTEM	ai_task_completed	ai_task	TASK-9E51F1F881	{"event_id": "EVT-RT-34B0B646", "snapshot_id": "SNP-RT-1D0507D0"}	2026-06-17T10:57:55.776999+00:00
AUD-FE0CDFB29D90	SYSTEM	ai_task_completed	ai_task	TASK-4E14B2540F	{"event_id": "EVT-RT-FAE1F3A6", "snapshot_id": "SNP-RT-834A4752"}	2026-06-17T10:58:25.886378+00:00
AUD-FD60E215DAD0	SYSTEM	ai_task_completed	ai_task	TASK-6353F4A1B5	{"event_id": "EVT-RT-E5959412", "snapshot_id": "SNP-RT-C7D6E2BB"}	2026-06-17T10:58:55.950664+00:00
AUD-CB8BB5E55CE5	SYSTEM	ai_task_completed	ai_task	TASK-E6095BAA3B	{"event_id": "EVT-RT-189AD3CF", "snapshot_id": "SNP-RT-D0CCD12E"}	2026-06-17T10:59:26.060500+00:00
AUD-9D7D2D6F281D	SYSTEM	ai_task_completed	ai_task	TASK-2A8CEE8D61	{"event_id": "EVT-RT-15B5B56B", "snapshot_id": "SNP-RT-0BCB4AE0"}	2026-06-17T10:59:56.133939+00:00
AUD-75DFFCFD7B9A	SYSTEM	ai_task_completed	ai_task	TASK-AC1CE2D93D	{"event_id": "EVT-RT-62048F22", "snapshot_id": "SNP-RT-352D8782"}	2026-06-17T11:00:26.236833+00:00
AUD-6A99124659BF	SYSTEM	ai_task_completed	ai_task	TASK-ED492622C8	{"event_id": "EVT-RT-B2331059", "snapshot_id": "SNP-RT-66B53F41"}	2026-06-17T11:00:56.303320+00:00
AUD-1728D8039191	SYSTEM	ai_task_completed	ai_task	TASK-013C1B324E	{"event_id": "EVT-RT-A58C4061", "snapshot_id": "SNP-RT-01EA45B8"}	2026-06-17T11:01:26.414762+00:00
AUD-393F33F35A5B	SYSTEM	ai_task_completed	ai_task	TASK-277985458D	{"event_id": "EVT-RT-21821EFE", "snapshot_id": "SNP-RT-5ACBBE93"}	2026-06-17T11:01:56.509578+00:00
AUD-0524A88E39BC	SYSTEM	ai_task_completed	ai_task	TASK-83E6177CCC	{"event_id": "EVT-RT-EAFE0103", "snapshot_id": "SNP-RT-50AB5946"}	2026-06-17T11:02:26.572412+00:00
AUD-9C3DA02E58DA	SYSTEM	ai_task_completed	ai_task	TASK-FA5D95E264	{"event_id": "EVT-RT-3CD59E0A", "snapshot_id": "SNP-RT-E92EA25B"}	2026-06-17T11:02:56.678004+00:00
AUD-4857108AE675	SYSTEM	ai_task_completed	ai_task	TASK-7B0C68613E	{"event_id": "EVT-RT-8CB0CFDE", "snapshot_id": "SNP-RT-AF7ADE53"}	2026-06-17T11:03:26.780626+00:00
AUD-16F58A6CE5F6	SYSTEM	ai_task_completed	ai_task	TASK-F91C0F5E9B	{"event_id": "EVT-RT-035FC18A", "snapshot_id": "SNP-RT-07CB56D7"}	2026-06-17T11:03:56.882695+00:00
AUD-4E84871B8854	SYSTEM	ai_task_completed	ai_task	TASK-2D5947470E	{"event_id": "EVT-RT-8B98E8F6", "snapshot_id": "SNP-RT-C9EE7BC5"}	2026-06-17T11:04:27.001051+00:00
AUD-595707166EC4	SYSTEM	ai_task_completed	ai_task	TASK-669830D189	{"event_id": "EVT-RT-A62E7420", "snapshot_id": "SNP-RT-13331A81"}	2026-06-17T11:04:57.107742+00:00
AUD-575906F628D9	SYSTEM	ai_task_completed	ai_task	TASK-40683AB350	{"event_id": "EVT-RT-890B4B35", "snapshot_id": "SNP-RT-879620AA"}	2026-06-17T11:05:27.216157+00:00
AUD-2142AB577CCA	SYSTEM	ai_task_completed	ai_task	TASK-4E1B813CDA	{"event_id": "EVT-RT-BD7B3FFD", "snapshot_id": "SNP-RT-78760BA7"}	2026-06-17T11:05:57.314983+00:00
AUD-FD7FFDCA389D	SYSTEM	ai_task_completed	ai_task	TASK-152291AED0	{"event_id": "EVT-RT-4C51ED30", "snapshot_id": "SNP-RT-138DE4A2"}	2026-06-17T11:06:27.424956+00:00
AUD-44FB60C294CA	SYSTEM	ai_task_completed	ai_task	TASK-12350C6A80	{"event_id": "EVT-RT-F76AD84A", "snapshot_id": "SNP-RT-7DDF2F33"}	2026-06-17T11:06:57.526461+00:00
AUD-9FACBADD6B64	SYSTEM	ai_task_completed	ai_task	TASK-F636EDB4D9	{"event_id": "EVT-RT-0528AC11", "snapshot_id": "SNP-RT-42507479"}	2026-06-17T11:07:27.632362+00:00
AUD-54D3C082C4B8	SYSTEM	ai_task_completed	ai_task	TASK-7BFDBD476D	{"event_id": "EVT-RT-AB639D38", "snapshot_id": "SNP-RT-AD367C46"}	2026-06-17T11:07:57.711640+00:00
AUD-0A7AADA2BAF3	SYSTEM	ai_task_completed	ai_task	TASK-87BF29548D	{"event_id": "EVT-RT-01B855E7", "snapshot_id": "SNP-RT-047502A6"}	2026-06-17T11:08:27.812359+00:00
AUD-6D56BE87DAD4	SYSTEM	ai_task_completed	ai_task	TASK-7D0CB2B0C6	{"event_id": "EVT-RT-D11FA1B5", "snapshot_id": "SNP-RT-33E3E69C"}	2026-06-17T11:08:57.905952+00:00
AUD-4E7A6FBEF584	SYSTEM	ai_task_completed	ai_task	TASK-BEE58C9E8B	{"event_id": "EVT-RT-BDD8026A", "snapshot_id": "SNP-RT-8125A032"}	2026-06-17T11:09:28.088483+00:00
AUD-F1A167A5C362	SYSTEM	ai_task_completed	ai_task	TASK-62D947DFEA	{"event_id": "EVT-RT-7E9F006D", "snapshot_id": "SNP-RT-82A17860"}	2026-06-17T11:09:58.185049+00:00
AUD-0E5499B748B5	SYSTEM	ai_task_completed	ai_task	TASK-D1CE2CC918	{"event_id": "EVT-RT-9B32B69A", "snapshot_id": "SNP-RT-6DA590DF"}	2026-06-17T11:10:28.276798+00:00
AUD-72A62B1B7946	SYSTEM	ai_task_completed	ai_task	TASK-CC7D15B8EE	{"event_id": "EVT-RT-7ACE6473", "snapshot_id": "SNP-RT-9BBC7994"}	2026-06-17T11:10:58.364875+00:00
AUD-81C6CB6DB189	SYSTEM	ai_task_completed	ai_task	TASK-3061CEA756	{"event_id": "EVT-RT-D5061419", "snapshot_id": "SNP-RT-C97B3054"}	2026-06-17T11:11:28.441648+00:00
AUD-96B735E3EF33	SYSTEM	ai_task_completed	ai_task	TASK-85711E85ED	{"event_id": "EVT-RT-1ABFE50B", "snapshot_id": "SNP-RT-11CBB77D"}	2026-06-17T11:11:58.587981+00:00
AUD-B8AB6E4EA70E	SYSTEM	ai_task_completed	ai_task	TASK-647436C5E5	{"event_id": "EVT-RT-4C60F9CC", "snapshot_id": "SNP-RT-43FE1A39"}	2026-06-17T11:12:28.694505+00:00
AUD-484AA59D0F46	SYSTEM	ai_task_completed	ai_task	TASK-23AAD58DB7	{"event_id": "EVT-RT-F7C36D50", "snapshot_id": "SNP-RT-16AC0BD0"}	2026-06-17T11:12:58.790905+00:00
AUD-64CB9558F5D0	SYSTEM	ai_task_completed	ai_task	TASK-EF392AD9CF	{"event_id": "EVT-RT-666372AF", "snapshot_id": "SNP-RT-C3614D82"}	2026-06-17T11:13:28.892103+00:00
AUD-FD7759A5D69A	SYSTEM	ai_task_completed	ai_task	TASK-8E2118A0DF	{"event_id": "EVT-RT-F190C297", "snapshot_id": "SNP-RT-F6C034B1"}	2026-06-17T11:13:58.998174+00:00
AUD-815E210092BE	SYSTEM	ai_task_completed	ai_task	TASK-A93F02AA41	{"event_id": "EVT-RT-8B9E19CA", "snapshot_id": "SNP-RT-B1053058"}	2026-06-17T11:14:29.072238+00:00
AUD-DD07F49B96E6	SYSTEM	ai_task_completed	ai_task	TASK-96FA9124A1	{"event_id": "EVT-RT-8928E2BF", "snapshot_id": "SNP-RT-301B1892"}	2026-06-17T11:14:59.174007+00:00
AUD-4DAEC078E6F3	SYSTEM	ai_task_completed	ai_task	TASK-5CADBC0793	{"event_id": "EVT-RT-1E3F177D", "snapshot_id": "SNP-RT-9BA6FB50"}	2026-06-17T11:15:29.279421+00:00
AUD-570189D8C947	SYSTEM	ai_task_completed	ai_task	TASK-935C14BC85	{"event_id": "EVT-RT-742BC921", "snapshot_id": "SNP-RT-78798827"}	2026-06-17T11:15:59.367261+00:00
AUD-8AAD850C3FA8	SYSTEM	ai_task_completed	ai_task	TASK-8B84B3B8EB	{"event_id": "EVT-RT-1601262E", "snapshot_id": "SNP-RT-4F93D708"}	2026-06-17T11:16:29.456533+00:00
AUD-8AE89D602DB8	SYSTEM	ai_task_completed	ai_task	TASK-A2D4F9E1C9	{"event_id": "EVT-RT-005247E1", "snapshot_id": "SNP-RT-A58F1E66"}	2026-06-17T11:16:59.538927+00:00
AUD-88C895E650E4	SYSTEM	ai_task_completed	ai_task	TASK-65039ECF1D	{"event_id": "EVT-RT-46EDDC05", "snapshot_id": "SNP-RT-E8BE3695"}	2026-06-17T11:17:29.667434+00:00
AUD-5DD879B8D026	SYSTEM	ai_task_completed	ai_task	TASK-64444D7A46	{"event_id": "EVT-RT-B49D9895", "snapshot_id": "SNP-RT-D29926B9"}	2026-06-17T11:17:59.774331+00:00
AUD-6F462E2F198D	SYSTEM	ai_task_completed	ai_task	TASK-FA40254546	{"event_id": "EVT-RT-40E7E3F0", "snapshot_id": "SNP-RT-5C8F5F59"}	2026-06-17T11:18:29.875758+00:00
AUD-2FF11C1E7063	SYSTEM	ai_task_completed	ai_task	TASK-F044EC8265	{"event_id": "EVT-RT-F925007A", "snapshot_id": "SNP-RT-12A0F44C"}	2026-06-17T11:18:59.992277+00:00
AUD-E8C24D5B154F	SYSTEM	ai_task_completed	ai_task	TASK-8FAD9152F2	{"event_id": "EVT-RT-983B7A3E", "snapshot_id": "SNP-RT-9A45DCEF"}	2026-06-17T11:19:30.092900+00:00
AUD-7BAECAEFD23A	SYSTEM	ai_task_completed	ai_task	TASK-5C96C47F08	{"event_id": "EVT-RT-0E648378", "snapshot_id": "SNP-RT-03D631D2"}	2026-06-17T11:20:00.203785+00:00
AUD-1D28FAC6E07F	SYSTEM	ai_task_completed	ai_task	TASK-RT-B87C74B3	{"event_id": "EVT-RT-97ADA9F5", "snapshot_id": "SNP-RT-7AFD36E7"}	2026-06-17T11:20:17.067676+00:00
AUD-D422C6187A28	SYSTEM	ai_task_completed	ai_task	TASK-AE74154D8E	{"event_id": "EVT-RT-11BCF260", "snapshot_id": "SNP-RT-BE9722E5"}	2026-06-17T11:20:30.314783+00:00
AUD-279D21390451	SYSTEM	ai_task_completed	ai_task	TASK-RT-BD19D809	{"event_id": "EVT-RT-28A01B9D", "snapshot_id": "SNP-RT-EF09EE99"}	2026-06-17T11:20:47.109404+00:00
AUD-E773DDEFDDB2	SYSTEM	ai_task_completed	ai_task	TASK-5DC0593237	{"event_id": "EVT-RT-46EBB3F8", "snapshot_id": "SNP-RT-B7C66EC8"}	2026-06-17T11:21:00.419687+00:00
AUD-E693ADD14E4B	SYSTEM	ai_task_completed	ai_task	TASK-RT-DB9384BA	{"event_id": "EVT-RT-0329AF4A", "snapshot_id": "SNP-RT-D9140C50"}	2026-06-17T11:21:17.157525+00:00
AUD-BFC4A7F0F41A	SYSTEM	ai_task_completed	ai_task	TASK-2250DF1189	{"event_id": "EVT-RT-B1BF2656", "snapshot_id": "SNP-RT-6A3D4AA5"}	2026-06-17T11:21:30.470004+00:00
AUD-E28B678D3196	SYSTEM	ai_task_completed	ai_task	TASK-RT-D42AEB8C	{"event_id": "EVT-RT-5A0D2CAB", "snapshot_id": "SNP-RT-6F4AAD48"}	2026-06-17T11:21:47.189997+00:00
AUD-EBAD47EF6960	SYSTEM	ai_task_completed	ai_task	TASK-8133D08A62	{"event_id": "EVT-RT-1C75A8AC", "snapshot_id": "SNP-RT-B55B0A6F"}	2026-06-17T11:22:00.533492+00:00
AUD-5638027BACD6	SYSTEM	ai_task_completed	ai_task	TASK-RT-CB763AB0	{"event_id": "EVT-RT-AE169985", "snapshot_id": "SNP-RT-F2D9AE1A"}	2026-06-17T11:22:17.227128+00:00
AUD-5A3D829F8214	SYSTEM	ai_task_completed	ai_task	TASK-7A5AB65D64	{"event_id": "EVT-RT-445037A6", "snapshot_id": "SNP-RT-96C47431"}	2026-06-17T11:22:30.607520+00:00
AUD-F2FC29C75BD3	SYSTEM	ai_task_completed	ai_task	TASK-RT-1E0E5AF4	{"event_id": "EVT-RT-1F2382FF", "snapshot_id": "SNP-RT-BAF4BB63"}	2026-06-17T11:22:47.260145+00:00
AUD-FC489D6FD415	SYSTEM	ai_task_completed	ai_task	TASK-5D9DEAE6EE	{"event_id": "EVT-RT-A9415D69", "snapshot_id": "SNP-RT-552FF62D"}	2026-06-17T11:23:00.715592+00:00
AUD-1A67AC3BA537	SYSTEM	ai_task_completed	ai_task	TASK-RT-E26A88E1	{"event_id": "EVT-RT-0AC67C31", "snapshot_id": "SNP-RT-BDE0508E"}	2026-06-17T11:23:17.288539+00:00
AUD-9B685A5555CA	SYSTEM	ai_task_completed	ai_task	TASK-16911A5C6C	{"event_id": "EVT-RT-3D7175A3", "snapshot_id": "SNP-RT-471195EF"}	2026-06-17T11:23:30.825498+00:00
AUD-7F3A65E6E444	SYSTEM	ai_task_completed	ai_task	TASK-RT-577EEE46	{"event_id": "EVT-RT-DD971EF9", "snapshot_id": "SNP-RT-47A4B21A"}	2026-06-17T11:23:47.319762+00:00
AUD-3DFFCC49139D	SYSTEM	ai_task_completed	ai_task	TASK-C962B5E77B	{"event_id": "EVT-RT-79C9E74E", "snapshot_id": "SNP-RT-65F7FC3B"}	2026-06-17T11:24:00.906974+00:00
AUD-BAEBD52187B1	SYSTEM	ai_task_completed	ai_task	TASK-RT-36CEF3C5	{"event_id": "EVT-RT-6CBA8F56", "snapshot_id": "SNP-RT-8B00993E"}	2026-06-17T11:24:17.345660+00:00
AUD-0AD8111F9FF5	SYSTEM	ai_task_completed	ai_task	TASK-8655BF4A87	{"event_id": "EVT-RT-ABD6E01F", "snapshot_id": "SNP-RT-4F8A5560"}	2026-06-17T11:24:30.989865+00:00
AUD-3C8D76E54F34	SYSTEM	ai_task_completed	ai_task	TASK-RT-E27A994F	{"event_id": "EVT-RT-E3AECE57", "snapshot_id": "SNP-RT-9BFF1B77"}	2026-06-17T11:24:47.392165+00:00
AUD-D80B325D53D8	SYSTEM	ai_task_completed	ai_task	TASK-9B06460DD1	{"event_id": "EVT-RT-E429A27B", "snapshot_id": "SNP-RT-507C8CBC"}	2026-06-17T11:25:01.090714+00:00
AUD-D2D1788F4E00	SYSTEM	ai_task_completed	ai_task	TASK-F13A7A6BF2	{"event_id": "EVT-RT-402E8448", "snapshot_id": "SNP-RT-7418ABA3"}	2026-06-17T11:25:10.523023+00:00
AUD-F68928E7258B	SYSTEM	ai_task_completed	ai_task	TASK-ED33AD45BF	{"event_id": "EVT-RT-1C4417FC", "snapshot_id": "SNP-RT-E3FBBF65"}	2026-06-17T11:25:15.236555+00:00
AUD-23514AC7D617	SYSTEM	ai_task_completed	ai_task	TASK-RT-32FF2DEF	{"event_id": "EVT-RT-5AD44F56", "snapshot_id": "SNP-RT-28AF1EC1"}	2026-06-17T11:25:17.417883+00:00
AUD-C87F8E6C298D	SYSTEM	ai_task_completed	ai_task	TASK-7418397A61	{"event_id": "EVT-RT-A85D7334", "snapshot_id": "SNP-RT-CC5C459A"}	2026-06-17T11:25:40.633326+00:00
AUD-2B17450FD9A6	SYSTEM	ai_task_completed	ai_task	TASK-RT-7C038A80	{"event_id": "EVT-RT-EEECA9BB", "snapshot_id": "SNP-RT-21567AED"}	2026-06-17T11:25:47.432737+00:00
AUD-7CD29CFE4C6A	SYSTEM	ai_task_completed	ai_task	TASK-A6D39E144D	{"event_id": "EVT-RT-21B241FC", "snapshot_id": "SNP-RT-28C317A3"}	2026-06-17T11:26:10.739652+00:00
AUD-4D9A962FC72A	SYSTEM	ai_task_completed	ai_task	TASK-RT-C3D6A4F4	{"event_id": "EVT-RT-7D0161F8", "snapshot_id": "SNP-RT-15263731"}	2026-06-17T11:26:17.451424+00:00
AUD-2E5CC4237D35	SYSTEM	ai_task_completed	ai_task	TASK-DC3AA86377	{"event_id": "EVT-RT-E15945A2", "snapshot_id": "SNP-RT-064E86A9"}	2026-06-17T11:26:40.852419+00:00
AUD-AB47A4249FBC	SYSTEM	ai_task_completed	ai_task	TASK-RT-A2C06663	{"event_id": "EVT-RT-F80A0D7A", "snapshot_id": "SNP-RT-D6074555"}	2026-06-17T11:26:47.492021+00:00
AUD-FEDB28544A8A	SYSTEM	ai_task_completed	ai_task	TASK-1D46A611E3	{"event_id": "EVT-RT-C4E974AE", "snapshot_id": "SNP-RT-86A0BE27"}	2026-06-17T11:27:10.928118+00:00
AUD-A0BEF5AED0A8	SYSTEM	ai_task_completed	ai_task	TASK-RT-D94A7836	{"event_id": "EVT-RT-1164035B", "snapshot_id": "SNP-RT-919FEC7B"}	2026-06-17T11:27:17.519754+00:00
AUD-C63CC8C8606B	SYSTEM	ai_task_completed	ai_task	TASK-D14F5D6E48	{"event_id": "EVT-RT-772E7897", "snapshot_id": "SNP-RT-3630F009"}	2026-06-17T11:27:41.033976+00:00
AUD-8ADC4082EBC5	SYSTEM	ai_task_completed	ai_task	TASK-RT-94545492	{"event_id": "EVT-RT-0D4E4060", "snapshot_id": "SNP-RT-C5E34664"}	2026-06-17T11:27:47.553662+00:00
AUD-088CD3B013A5	SYSTEM	ai_task_completed	ai_task	TASK-118ACB685C	{"event_id": "EVT-RT-81925D12", "snapshot_id": "SNP-RT-8B7B7161"}	2026-06-17T11:28:11.130428+00:00
AUD-B1A3C0A0C118	SYSTEM	ai_task_completed	ai_task	TASK-RT-9FB6A4D0	{"event_id": "EVT-RT-003CF0A2", "snapshot_id": "SNP-RT-3698940B"}	2026-06-17T11:28:17.581466+00:00
AUD-EEB7FD71BE51	SYSTEM	ai_task_completed	ai_task	TASK-F87FAF486E	{"event_id": "EVT-RT-613C495B", "snapshot_id": "SNP-RT-6BB862B5"}	2026-06-17T11:28:35.784713+00:00
AUD-791A7D22684D	SYSTEM	ai_task_completed	ai_task	TASK-DEE4732A2B	{"event_id": "EVT-RT-73C67934", "snapshot_id": "SNP-RT-0FDA611B"}	2026-06-17T11:28:54.698343+00:00
AUD-8064BA1C6218	SYSTEM	ai_task_completed	ai_task	TASK-ACF7351EB3	{"event_id": "EVT-RT-C99CEA05", "snapshot_id": "SNP-RT-E4925B7D"}	2026-06-17T11:28:54.750154+00:00
AUD-69C2A9537919	SYSTEM	ai_task_completed	ai_task	TASK-RT-A899BAE8	{"event_id": "EVT-RT-E81AE02E", "snapshot_id": "SNP-RT-0EEFABFB"}	2026-06-17T11:28:55.185763+00:00
AUD-5DE6C7FB6531	SYSTEM	ai_task_completed	ai_task	TASK-2CAD34CF7E	{"event_id": "EVT-RT-D7AA35A8", "snapshot_id": "SNP-RT-82A0DD6A"}	2026-06-17T11:29:05.889646+00:00
AUD-5BEA6E47F271	SYSTEM	ai_task_completed	ai_task	TASK-RT-17064911	{"event_id": "EVT-RT-1E90893A", "snapshot_id": "SNP-RT-51C7ABF9"}	2026-06-17T11:29:25.231953+00:00
AUD-C93437726D73	SYSTEM	ai_task_completed	ai_task	TASK-B55AB73EE3	{"event_id": "EVT-RT-89A6EB4E", "snapshot_id": "SNP-RT-B1B69FDB"}	2026-06-17T11:29:36.028832+00:00
AUD-8B499337DE9D	SYSTEM	ai_task_completed	ai_task	TASK-RT-F2C4D050	{"event_id": "EVT-RT-B6322AD7", "snapshot_id": "SNP-RT-83F4E235"}	2026-06-17T11:29:55.272599+00:00
AUD-0692A7906344	SYSTEM	ai_task_completed	ai_task	TASK-8D1E15AE93	{"event_id": "EVT-RT-D26A1E81", "snapshot_id": "SNP-RT-A3EA61AD"}	2026-06-17T11:30:06.150911+00:00
AUD-367B43F28942	SYSTEM	ai_task_completed	ai_task	TASK-RT-E8D769B8	{"event_id": "EVT-RT-D689D0D3", "snapshot_id": "SNP-RT-0556E3D8"}	2026-06-17T11:30:25.313732+00:00
AUD-6E258B6F4EC8	SYSTEM	ai_task_completed	ai_task	TASK-0A5B308039	{"event_id": "EVT-RT-4317FDEB", "snapshot_id": "SNP-RT-2CC7057A"}	2026-06-17T11:30:36.259035+00:00
AUD-DDF1FD28AE64	SYSTEM	ai_task_completed	ai_task	TASK-RT-528C005B	{"event_id": "EVT-RT-413A8029", "snapshot_id": "SNP-RT-5AA8AC1F"}	2026-06-17T11:30:55.354886+00:00
AUD-10D542E8AAA6	SYSTEM	ai_task_completed	ai_task	TASK-95D7A26B46	{"event_id": "EVT-RT-2F01612B", "snapshot_id": "SNP-RT-C6D400A4"}	2026-06-17T11:31:06.359226+00:00
AUD-08A327EB16D8	SYSTEM	ai_task_completed	ai_task	TASK-RT-2ABFFE98	{"event_id": "EVT-RT-02D41BB8", "snapshot_id": "SNP-RT-CE6250BF"}	2026-06-17T11:31:25.393471+00:00
AUD-4832801E295C	SYSTEM	ai_task_completed	ai_task	TASK-DF5117DD75	{"event_id": "EVT-RT-B12F7CA0", "snapshot_id": "SNP-RT-8192C1DC"}	2026-06-17T11:31:36.484043+00:00
AUD-58D3CAAC73C4	SYSTEM	ai_task_completed	ai_task	TASK-RT-B115E8AE	{"event_id": "EVT-RT-138FD32B", "snapshot_id": "SNP-RT-A0421BA8"}	2026-06-17T11:31:55.462353+00:00
AUD-D12B0FA4D628	SYSTEM	ai_task_completed	ai_task	TASK-C7F223786D	{"event_id": "EVT-RT-ECBF4A37", "snapshot_id": "SNP-RT-E2B3EEC9"}	2026-06-17T11:32:06.631229+00:00
AUD-A9CBDAEAFAD7	SYSTEM	ai_task_completed	ai_task	TASK-RT-1E303225	{"event_id": "EVT-RT-76C289CD", "snapshot_id": "SNP-RT-FD4915EA"}	2026-06-17T11:32:25.502759+00:00
AUD-B6D2AD91A738	SYSTEM	ai_task_completed	ai_task	TASK-D6B2EC518C	{"event_id": "EVT-RT-BC96516B", "snapshot_id": "SNP-RT-889DAE64"}	2026-06-17T11:32:36.734766+00:00
AUD-88632D8DCBA4	SYSTEM	ai_task_completed	ai_task	TASK-RT-53A1BF1B	{"event_id": "EVT-RT-F83A7242", "snapshot_id": "SNP-RT-2DF62FD9"}	2026-06-17T11:32:55.537939+00:00
AUD-85781683F208	SYSTEM	ai_task_completed	ai_task	TASK-0A9D5DF1C6	{"event_id": "EVT-RT-C0B71764", "snapshot_id": "SNP-RT-5F94035C"}	2026-06-17T11:33:06.834376+00:00
AUD-08C63F7E2E30	SYSTEM	ai_task_completed	ai_task	TASK-RT-C13D4886	{"event_id": "EVT-RT-F712DB9E", "snapshot_id": "SNP-RT-0B74C7D8"}	2026-06-17T11:33:25.563248+00:00
AUD-F32B26D45C64	SYSTEM	ai_task_completed	ai_task	TASK-1A021D3391	{"event_id": "EVT-RT-1B63D861", "snapshot_id": "SNP-RT-67E814EF"}	2026-06-17T11:33:36.943815+00:00
AUD-E8A3E19D96CE	SYSTEM	ai_task_completed	ai_task	TASK-RT-9C9603AD	{"event_id": "EVT-RT-90F85F4D", "snapshot_id": "SNP-RT-0740C0F1"}	2026-06-17T11:33:55.613855+00:00
AUD-AD84CBDADCE9	SYSTEM	ai_task_completed	ai_task	TASK-8E09BFDAF0	{"event_id": "EVT-RT-8CD99719", "snapshot_id": "SNP-RT-E9FDF2A7"}	2026-06-17T11:34:07.075042+00:00
AUD-302E8F982AC9	SYSTEM	ai_task_completed	ai_task	TASK-RT-1F5A7734	{"event_id": "EVT-RT-52986ADA", "snapshot_id": "SNP-RT-466DAC58"}	2026-06-17T11:34:25.641066+00:00
AUD-DD5446B83FA1	SYSTEM	ai_task_completed	ai_task	TASK-CFC31D734A	{"event_id": "EVT-RT-0E388E10", "snapshot_id": "SNP-RT-38896A15"}	2026-06-17T11:34:37.247822+00:00
AUD-0CE853785419	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-70152E96FC3B	{"rule_id": "BR-001", "rule_type": "person_dirty_to_safe_without_disinfection", "event_id": "EVT-BIO-A5EF2334", "snapshot_id": "SNP-BIO-B15E1BBB", "track_id": 9091, "from_zone": "dirty_zone", "to_zone": "safe_zone"}	2026-06-17T11:34:48.920006+00:00
AUD-5A1D04000135	SYSTEM	ai_task_completed	ai_task	TASK-RT-CFC559F1	{"event_id": "EVT-RT-DAE56305", "snapshot_id": "SNP-RT-5F58CA16"}	2026-06-17T11:34:59.281889+00:00
AUD-69B3F0BD93B9	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-D7ED08D0208E	{"rule_id": "BR-003", "rule_type": "dog_enter_production", "event_id": "EVT-BIO-DEE399AF", "snapshot_id": "SNP-BIO-2AB2F3B7", "track_id": 9093, "from_zone": "parking_zone", "to_zone": "production_zone"}	2026-06-17T11:35:03.738042+00:00
AUD-F9A714EE5852	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-EC007C1091FD	{"rule_id": "BR-004", "rule_type": "cat_enter_production", "event_id": "EVT-BIO-46B5E878", "snapshot_id": "SNP-BIO-98A3C7BF", "track_id": 9094, "from_zone": "parking_zone", "to_zone": "production_zone"}	2026-06-17T11:35:03.758650+00:00
AUD-6CCAC3C5D30C	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-E437F118D9FA	{"rule_id": "BR-005", "rule_type": "bird_enter_feed_storage", "event_id": "EVT-BIO-2FDEB0F8", "snapshot_id": "SNP-BIO-3BBF2A6C", "track_id": 9095, "from_zone": "outside_zone", "to_zone": "feed_storage_zone"}	2026-06-17T11:35:03.776390+00:00
AUD-C325B5E4436F	SYSTEM	ai_task_completed	ai_task	TASK-E26FF410EF	{"event_id": "EVT-RT-A94CA0A1", "snapshot_id": "SNP-RT-0760109A"}	2026-06-17T11:35:07.359305+00:00
AUD-794757A9326F	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-CC26BF1B37C0	{"rule_id": "BR-002", "rule_type": "vehicle_outside_to_production_without_vehicle_disinfection", "event_id": "EVT-BIO-8588D458", "snapshot_id": "SNP-BIO-95B452F8", "track_id": 9096, "from_zone": "outside_zone", "to_zone": "production_zone"}	2026-06-17T11:35:31.586471+00:00
AUD-512AC228BF45	SYSTEM	ai_task_completed	ai_task	TASK-A5135182B5	{"event_id": "EVT-RT-BCFCCBE0", "snapshot_id": "SNP-RT-69AE7BBD"}	2026-06-17T11:35:37.476086+00:00
AUD-2AE165339985	SYSTEM	ai_task_completed	ai_task	TASK-RT-70088D2A	{"event_id": "EVT-RT-F7C908CD", "snapshot_id": "SNP-RT-09BAD963"}	2026-06-17T11:35:56.438577+00:00
AUD-A6B0B218E3C6	SYSTEM	ai_task_completed	ai_task	TASK-67BFFE2E19	{"event_id": "EVT-RT-6AA9163B", "snapshot_id": "SNP-RT-9F406360"}	2026-06-17T11:36:07.611621+00:00
AUD-C96241B42D28	SYSTEM	ai_task_completed	ai_task	TASK-RT-B77D5F9C	{"event_id": "EVT-RT-C5F71D7F", "snapshot_id": "SNP-RT-6BE76F4D"}	2026-06-17T11:36:26.562149+00:00
AUD-929273F3FE88	SYSTEM	ai_task_completed	ai_task	TASK-58CA437ACB	{"event_id": "EVT-RT-1FEBCC6C", "snapshot_id": "SNP-RT-A8379BE2"}	2026-06-17T11:36:37.730852+00:00
AUD-CB88ED4623C1	SYSTEM	ai_task_completed	ai_task	TASK-RT-1818F995	{"event_id": "EVT-RT-D21F9CE7", "snapshot_id": "SNP-RT-4B2EEA5B"}	2026-06-17T11:36:56.614326+00:00
AUD-9510224E95CD	SYSTEM	ai_task_completed	ai_task	TASK-5712E164C4	{"event_id": "EVT-RT-925668E7", "snapshot_id": "SNP-RT-E8ADB7BF"}	2026-06-17T11:37:07.817392+00:00
AUD-D574BAB0860F	SYSTEM	ai_task_completed	ai_task	TASK-RT-BC932F80	{"event_id": "EVT-RT-AC22E0AA", "snapshot_id": "SNP-RT-2DE3ADB1"}	2026-06-17T11:37:26.701751+00:00
AUD-6B79229A97E5	SYSTEM	ai_task_completed	ai_task	TASK-4CD864135B	{"event_id": "EVT-RT-9C1BFE70", "snapshot_id": "SNP-RT-892A07FE"}	2026-06-17T11:37:37.894280+00:00
AUD-41A52B472BDF	SYSTEM	ai_task_completed	ai_task	TASK-RT-C5688D5E	{"event_id": "EVT-RT-BE6D4165", "snapshot_id": "SNP-RT-6B22AA24"}	2026-06-17T11:37:56.754886+00:00
AUD-585F2B4FA952	SYSTEM	ai_task_completed	ai_task	TASK-3E521F5E0B	{"event_id": "EVT-RT-20231813", "snapshot_id": "SNP-RT-63306979"}	2026-06-17T11:38:08.014417+00:00
AUD-15F316C26A7B	SYSTEM	ai_task_completed	ai_task	TASK-DD5C1EA7BC	{"event_id": "EVT-RT-2937B494", "snapshot_id": "SNP-RT-5F90683C"}	2026-06-17T11:38:38.123879+00:00
AUD-8F7495543CF5	SYSTEM	ai_task_completed	ai_task	TASK-RT-33D2C70F	{"event_id": "EVT-RT-322597A3", "snapshot_id": "SNP-RT-6BA2F5DF"}	2026-06-17T11:38:57.019980+00:00
AUD-672E1B368778	SYSTEM	ai_task_completed	ai_task	TASK-2D8E9F2EE8	{"event_id": "EVT-RT-9CDA0FE4", "snapshot_id": "SNP-RT-7DA12743"}	2026-06-17T11:39:08.245345+00:00
AUD-B5760900B4FE	SYSTEM	ai_task_completed	ai_task	TASK-RT-228E6BFB	{"event_id": "EVT-RT-669DF586", "snapshot_id": "SNP-RT-6F8E7D97"}	2026-06-17T11:39:27.051145+00:00
AUD-FF495FA0FA41	SYSTEM	ai_task_completed	ai_task	TASK-E947FC91EB	{"event_id": "EVT-RT-95117818", "snapshot_id": "SNP-RT-784C7FFD"}	2026-06-17T11:39:38.345602+00:00
AUD-F7D2DB39C2CF	SYSTEM	ai_task_completed	ai_task	TASK-RT-D803B5EE	{"event_id": "EVT-RT-D756BB8B", "snapshot_id": "SNP-RT-5FD8F7B6"}	2026-06-17T11:39:57.097802+00:00
AUD-B8F7F4B898C9	SYSTEM	ai_task_completed	ai_task	TASK-B67803B82B	{"event_id": "EVT-RT-53C72229", "snapshot_id": "SNP-RT-D0B87784"}	2026-06-17T11:40:08.439796+00:00
AUD-9DC716AD17D8	SYSTEM	ai_task_completed	ai_task	TASK-RT-E78CA900	{"event_id": "EVT-RT-6CEF0842", "snapshot_id": "SNP-RT-CFE4B675"}	2026-06-17T11:40:27.137055+00:00
AUD-D3C47045A550	SYSTEM	ai_task_completed	ai_task	TASK-4FC2192CB8	{"event_id": "EVT-RT-F6C71382", "snapshot_id": "SNP-RT-3CF6B30B"}	2026-06-17T11:40:38.560874+00:00
AUD-CAF5645FD2C4	SYSTEM	ai_task_completed	ai_task	TASK-RT-EF79DF87	{"event_id": "EVT-RT-8AC7E4CE", "snapshot_id": "SNP-RT-6796F6B1"}	2026-06-17T11:40:57.181589+00:00
AUD-4251F283291C	SYSTEM	ai_task_completed	ai_task	TASK-B6B3C54854	{"event_id": "EVT-RT-7E8A9DB8", "snapshot_id": "SNP-RT-02B46D8F"}	2026-06-17T11:41:08.687379+00:00
AUD-B951157D14EB	SYSTEM	ai_task_completed	ai_task	TASK-RT-98EAF3E3	{"event_id": "EVT-RT-4307A9AB", "snapshot_id": "SNP-RT-1732F109"}	2026-06-17T11:41:27.324145+00:00
AUD-8DD0531F0B61	SYSTEM	ai_task_completed	ai_task	TASK-47A48D535E	{"event_id": "EVT-RT-73C1462A", "snapshot_id": "SNP-RT-C49B7975"}	2026-06-17T11:41:38.848111+00:00
AUD-E5CB71D231A1	SYSTEM	ai_task_completed	ai_task	TASK-RT-3A3F5C8F	{"event_id": "EVT-RT-80A93610", "snapshot_id": "SNP-RT-C6CB91B2"}	2026-06-17T11:41:57.364511+00:00
AUD-E373CFB73D6F	SYSTEM	ai_task_completed	ai_task	TASK-7E33C6C8E7	{"event_id": "EVT-RT-C010D1D7", "snapshot_id": "SNP-RT-89AF4968"}	2026-06-17T11:42:08.971626+00:00
AUD-9A2B7E536C1B	SYSTEM	ai_task_completed	ai_task	TASK-RT-6B1E19BF	{"event_id": "EVT-RT-79C1C92E", "snapshot_id": "SNP-RT-64D0FBA1"}	2026-06-17T11:42:27.420221+00:00
AUD-F3E5148E8650	SYSTEM	ai_task_completed	ai_task	TASK-17C277DC4C	{"event_id": "EVT-RT-027413E3", "snapshot_id": "SNP-RT-F523CA84"}	2026-06-17T11:42:39.080975+00:00
AUD-37D40C6878C7	SYSTEM	ai_task_completed	ai_task	TASK-RT-55BD632A	{"event_id": "EVT-RT-60D3BE49", "snapshot_id": "SNP-RT-B208CEB1"}	2026-06-17T11:42:57.467941+00:00
AUD-779295ABA44F	SYSTEM	ai_task_completed	ai_task	TASK-FD470DDED5	{"event_id": "EVT-RT-EDBB9C74", "snapshot_id": "SNP-RT-81B50963"}	2026-06-17T11:43:09.181771+00:00
AUD-7F8191A9D9F9	SYSTEM	ai_task_completed	ai_task	TASK-RT-3C044100	{"event_id": "EVT-RT-B14FE8A3", "snapshot_id": "SNP-RT-3012D5C4"}	2026-06-17T11:43:27.495422+00:00
AUD-DC8CA32E9849	SYSTEM	ai_task_completed	ai_task	TASK-C45D81C2AF	{"event_id": "EVT-RT-C056B0AD", "snapshot_id": "SNP-RT-25BA14C0"}	2026-06-17T11:43:39.281925+00:00
AUD-9DDD6F475599	SYSTEM	ai_task_completed	ai_task	TASK-RT-67251F72	{"event_id": "EVT-RT-556E7387", "snapshot_id": "SNP-RT-73B4BEC2"}	2026-06-17T11:43:57.525791+00:00
AUD-09879A567461	SYSTEM	ai_task_completed	ai_task	TASK-B83C975C00	{"event_id": "EVT-RT-262DB66A", "snapshot_id": "SNP-RT-5524ED6C"}	2026-06-17T11:44:09.434631+00:00
AUD-077F216BF8F1	SYSTEM	ai_task_completed	ai_task	TASK-RT-6FEA7C29	{"event_id": "EVT-RT-38E0A425", "snapshot_id": "SNP-RT-45A196C5"}	2026-06-17T11:44:27.566348+00:00
AUD-28B7A25E3E2B	SYSTEM	ai_task_completed	ai_task	TASK-17C8B87EFC	{"event_id": "EVT-RT-264ABBF5", "snapshot_id": "SNP-RT-F0C17B50"}	2026-06-17T11:44:39.783232+00:00
AUD-92A18FB0FA32	SYSTEM	ai_task_completed	ai_task	TASK-RT-5FE7BCF6	{"event_id": "EVT-RT-94A2C0CE", "snapshot_id": "SNP-RT-C3DF744A"}	2026-06-17T11:44:57.607698+00:00
AUD-61A22ECB0FA7	SYSTEM	ai_task_completed	ai_task	TASK-D274DAFBAD	{"event_id": "EVT-RT-2227AE59", "snapshot_id": "SNP-RT-B66C5CAC"}	2026-06-17T11:45:09.913250+00:00
AUD-E331C30A12D5	SYSTEM	ai_task_completed	ai_task	TASK-RT-BD1E233A	{"event_id": "EVT-RT-A1F7A0C6", "snapshot_id": "SNP-RT-AB3DF4A2"}	2026-06-17T11:45:27.645344+00:00
AUD-BBE72BDA1578	SYSTEM	ai_task_completed	ai_task	TASK-F0AD9301AC	{"event_id": "EVT-RT-126F1D52", "snapshot_id": "SNP-RT-74FF4E4D"}	2026-06-17T11:45:40.005717+00:00
AUD-4D1ED38F6919	SYSTEM	ai_task_completed	ai_task	TASK-RT-0DA050C5	{"event_id": "EVT-RT-126B4CF0", "snapshot_id": "SNP-RT-366AE0B4"}	2026-06-17T11:45:57.686322+00:00
AUD-D96CF075524D	SYSTEM	ai_task_completed	ai_task	TASK-144B5985B8	{"event_id": "EVT-RT-91C987CE", "snapshot_id": "SNP-RT-D2DDB334"}	2026-06-17T11:46:10.115650+00:00
AUD-E5975FE49F05	SYSTEM	ai_task_completed	ai_task	TASK-RT-F7AAACE4	{"event_id": "EVT-RT-668DAA0B", "snapshot_id": "SNP-RT-22EFC9E1"}	2026-06-17T11:46:27.729554+00:00
AUD-27C7CACE0A72	SYSTEM	ai_task_completed	ai_task	TASK-748466EE91	{"event_id": "EVT-RT-DAA0ADEC", "snapshot_id": "SNP-RT-036668F2"}	2026-06-17T11:46:40.210652+00:00
AUD-66D310907BA5	SYSTEM	ai_task_completed	ai_task	TASK-3ACBD97133	{"event_id": "EVT-RT-99626250", "snapshot_id": "SNP-RT-A8E8F6C3"}	2026-06-17T11:47:10.313878+00:00
AUD-1AB84F025DE5	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-DD4C1D9981BB	{"rule_id": "BR-001", "rule_type": "person_dirty_to_safe_without_disinfection", "object_type": "person", "required_zone": "disinfection_zone", "event_id": "EVT-BIO-4D0342E3", "snapshot_id": "SNP-BIO-5E6FF574", "track_id": 9911, "from_zone": "dirty_zone", "to_zone": "safe_zone"}	2026-06-17T11:47:11.138874+00:00
AUD-FA396B6BF277	SYSTEM	ai_task_completed	ai_task	TASK-RT-49A2748F	{"event_id": "EVT-RT-FF900B5A", "snapshot_id": "SNP-RT-83BF9444"}	2026-06-17T11:47:12.882004+00:00
AUD-ACC30AEED2DB	SYSTEM	ai_task_completed	ai_task	TASK-6CD0CE3CCE	{"event_id": "EVT-RT-52425C1B", "snapshot_id": "SNP-RT-64DBB2D8"}	2026-06-17T11:47:40.445219+00:00
AUD-E1C3CA9B8EC9	SYSTEM	ai_task_completed	ai_task	TASK-RT-244915BD	{"event_id": "EVT-RT-1A5BD372", "snapshot_id": "SNP-RT-41F4145A"}	2026-06-17T11:48:06.580237+00:00
AUD-987FE6BEC559	SYSTEM	ai_task_completed	ai_task	TASK-E78378EC05	{"event_id": "EVT-RT-6740CC39", "snapshot_id": "SNP-RT-C8119B2E"}	2026-06-17T11:48:10.589616+00:00
AUD-6DEF5DEA4492	SYSTEM	ai_task_completed	ai_task	TASK-RT-BD1364CC	{"event_id": "EVT-RT-98A0A83F", "snapshot_id": "SNP-RT-7FD2030A"}	2026-06-17T11:48:36.609405+00:00
AUD-0C613E724EE6	SYSTEM	ai_task_completed	ai_task	TASK-03DD37AEF1	{"event_id": "EVT-RT-BE49213B", "snapshot_id": "SNP-RT-CF1F584D"}	2026-06-17T11:48:40.834124+00:00
AUD-225183E15702	SYSTEM	ai_task_completed	ai_task	TASK-RT-D2D12FEB	{"event_id": "EVT-RT-669EAC64", "snapshot_id": "SNP-RT-9E609FCA"}	2026-06-17T11:49:06.656528+00:00
AUD-0704A9EDA426	SYSTEM	ai_task_completed	ai_task	TASK-B2D120A065	{"event_id": "EVT-RT-106C239D", "snapshot_id": "SNP-RT-F5AA451B"}	2026-06-17T11:49:10.928905+00:00
AUD-0229629859DB	SYSTEM	ai_task_completed	ai_task	TASK-RT-EE70A9D1	{"event_id": "EVT-RT-0768B32A", "snapshot_id": "SNP-RT-18C04C6A"}	2026-06-17T11:49:36.705356+00:00
AUD-255EC1736576	SYSTEM	ai_task_completed	ai_task	TASK-2590704945	{"event_id": "EVT-RT-2ABE3773", "snapshot_id": "SNP-RT-4B4C147E"}	2026-06-17T11:49:41.000319+00:00
AUD-02157AD8E868	SYSTEM	ai_task_completed	ai_task	TASK-RT-B7D3CFC8	{"event_id": "EVT-RT-AE03A774", "snapshot_id": "SNP-RT-A44F3401"}	2026-06-17T11:50:06.745511+00:00
AUD-B27F8EA98AEE	SYSTEM	ai_task_completed	ai_task	TASK-462132C88E	{"event_id": "EVT-RT-79A62D89", "snapshot_id": "SNP-RT-3869E355"}	2026-06-17T11:50:11.089552+00:00
AUD-0EDD36A0054E	SYSTEM	ai_task_completed	ai_task	TASK-RT-1D475EFA	{"event_id": "EVT-RT-FA337C07", "snapshot_id": "SNP-RT-0F40B5B9"}	2026-06-17T11:50:36.782255+00:00
AUD-9C47A50126D1	SYSTEM	ai_task_completed	ai_task	TASK-11275000E4	{"event_id": "EVT-RT-0B6CBA8E", "snapshot_id": "SNP-RT-3A52F4CA"}	2026-06-17T11:50:41.188302+00:00
AUD-00EE62067A0B	SYSTEM	ai_task_completed	ai_task	TASK-RT-461277BD	{"event_id": "EVT-RT-D82FB6D0", "snapshot_id": "SNP-RT-8D0D08DF"}	2026-06-17T11:51:06.823361+00:00
AUD-A29A61364995	SYSTEM	ai_task_completed	ai_task	TASK-678292BB46	{"event_id": "EVT-RT-287FD0FE", "snapshot_id": "SNP-RT-61EDEB67"}	2026-06-17T11:51:11.287349+00:00
AUD-33A4E27A3C36	SYSTEM	ai_task_completed	ai_task	TASK-RT-505FE943	{"event_id": "EVT-RT-FE5F5541", "snapshot_id": "SNP-RT-7C9C2951"}	2026-06-17T11:51:36.857727+00:00
AUD-ED67567D4802	SYSTEM	ai_task_completed	ai_task	TASK-RT-7353F1A2	{"event_id": "EVT-RT-D34DE4C4", "snapshot_id": "SNP-RT-A0BB4A19"}	2026-06-17T11:52:06.898249+00:00
AUD-2F1989B943BB	SYSTEM	ai_task_completed	ai_task	TASK-RT-0A1670C6	{"event_id": "EVT-RT-8BCE368A", "snapshot_id": "SNP-RT-993C4DA9"}	2026-06-17T11:52:36.931324+00:00
AUD-228AC8728A94	SYSTEM	ai_task_completed	ai_task	TASK-RT-3ADA0080	{"event_id": "EVT-RT-D861E2EC", "snapshot_id": "SNP-RT-63A5AE73"}	2026-06-17T11:53:06.966872+00:00
AUD-2F8B0EA4D5F1	SYSTEM	ai_task_completed	ai_task	TASK-RT-48EF3C3E	{"event_id": "EVT-RT-6E8E2AF9", "snapshot_id": "SNP-RT-540DD198"}	2026-06-17T11:53:36.996819+00:00
AUD-F428DD92359D	SYSTEM	ai_task_completed	ai_task	TASK-RT-D392A7F1	{"event_id": "EVT-RT-504F9EF6", "snapshot_id": "SNP-RT-55342885"}	2026-06-17T11:54:07.023236+00:00
AUD-9D191508196E	SYSTEM	ai_task_completed	ai_task	TASK-2CAAC64364	{"event_id": "EVT-RT-523A8E57", "snapshot_id": "SNP-RT-DB544B4D"}	2026-06-17T11:51:41.395192+00:00
AUD-7712D05A36E0	SYSTEM	ai_task_completed	ai_task	TASK-71F520696A	{"event_id": "EVT-RT-FA0468B4", "snapshot_id": "SNP-RT-AFA57271"}	2026-06-17T11:52:11.486892+00:00
AUD-A86F5D00E233	SYSTEM	ai_task_completed	ai_task	TASK-DD8CED6325	{"event_id": "EVT-RT-8E6FEA13", "snapshot_id": "SNP-RT-FF8C9F78"}	2026-06-17T11:52:41.583137+00:00
AUD-1D5EF0A71829	SYSTEM	ai_task_completed	ai_task	TASK-BB55B4C618	{"event_id": "EVT-RT-A6C39563", "snapshot_id": "SNP-RT-7309E181"}	2026-06-17T11:53:11.653791+00:00
AUD-543354852E85	SYSTEM	ai_task_completed	ai_task	TASK-07A7B54A00	{"event_id": "EVT-RT-77C48643", "snapshot_id": "SNP-RT-BC655464"}	2026-06-17T11:53:41.720781+00:00
AUD-7706BE1B8C79	SYSTEM	ai_task_completed	ai_task	TASK-9F9EF2994B	{"event_id": "EVT-RT-3F439E86", "snapshot_id": "SNP-RT-2D570AD3"}	2026-06-17T11:54:11.802468+00:00
AUD-9FB3A39854D3	SYSTEM	ai_task_completed	ai_task	TASK-62B9D8B2D8	{"event_id": "EVT-RT-93C7C1D8", "snapshot_id": "SNP-RT-F34FAB60"}	2026-06-17T11:54:42.016000+00:00
AUD-40C463D587A8	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-067BE0AE3E83	{"rule_id": "BR-ATSH-001", "rule_type": "person_parking_to_gestation_without_disinfection", "object_type": "person", "required_zone": "person_disinfection_zone", "event_id": "EVT-BIO-03F1C1EE", "snapshot_id": "SNP-BIO-20F154CA", "track_id": 9001, "from_zone": "parking_zone", "to_zone": "gestation_barn", "zone_category": "production", "biosecurity_level": "clean", "risk_level": "high"}	2026-06-17T11:54:43.850113+00:00
AUD-F238E9B4DDBA	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-EDD566F6B59E	{"rule_id": "BR-ATSH-012", "rule_type": "dog_enter_farrowing_barn", "object_type": "dog", "required_zone": null, "event_id": "EVT-BIO-4D2CA332", "snapshot_id": "SNP-BIO-C45D3272", "track_id": 9003, "from_zone": "reception_zone", "to_zone": "farrowing_barn", "zone_category": "production", "biosecurity_level": "clean", "risk_level": "critical"}	2026-06-17T11:54:43.872794+00:00
AUD-C5534EF2D222	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-8BD35016CB6E	{"rule_id": "BR-ATSH-008", "rule_type": "vehicle_parking_to_loading_without_disinfection", "object_type": "vehicle", "required_zone": "vehicle_disinfection_zone", "event_id": "EVT-BIO-3988068E", "snapshot_id": "SNP-BIO-E81C07E8", "track_id": 9004, "from_zone": "parking_zone", "to_zone": "pig_loading_zone", "zone_category": "perimeter", "biosecurity_level": "dirty", "risk_level": "high"}	2026-06-17T11:54:43.882417+00:00
AUD-C68ED39C2BF4	SYSTEM	ai_task_completed	ai_task	TASK-RT-FFADC752	{"event_id": "EVT-RT-50325B06", "snapshot_id": "SNP-RT-51F228C8"}	2026-06-17T11:55:06.396751+00:00
AUD-E96080E7B721	SYSTEM	ai_task_completed	ai_task	TASK-3A5378DB7E	{"event_id": "EVT-RT-97FD0E5D", "snapshot_id": "SNP-RT-A01FB2A1"}	2026-06-17T11:55:12.119826+00:00
AUD-1B4072C3AE87	SYSTEM	ai_task_completed	ai_task	TASK-RT-01AC645E	{"event_id": "EVT-RT-D12BBBBE", "snapshot_id": "SNP-RT-3E2288E4"}	2026-06-17T11:55:36.437725+00:00
AUD-B02E128D5C56	SYSTEM	ai_task_completed	ai_task	TASK-43B5051763	{"event_id": "EVT-RT-00D9ED23", "snapshot_id": "SNP-RT-BE8E88AB"}	2026-06-17T11:55:42.213710+00:00
AUD-84EB14AE6CF7	SYSTEM	ai_task_completed	ai_task	TASK-RT-C47F8394	{"event_id": "EVT-RT-3CF6F2B3", "snapshot_id": "SNP-RT-8D9A789D"}	2026-06-17T11:56:06.479511+00:00
AUD-4F6579D3B601	SYSTEM	ai_task_completed	ai_task	TASK-C88C1CE866	{"event_id": "EVT-RT-3054BD93", "snapshot_id": "SNP-RT-64F6A7B6"}	2026-06-17T11:56:12.332216+00:00
AUD-3B586E285F95	SYSTEM	ai_task_completed	ai_task	TASK-RT-F1DCCA07	{"event_id": "EVT-RT-68167776", "snapshot_id": "SNP-RT-D2375158"}	2026-06-17T11:56:36.523687+00:00
AUD-083E4CF0B0FD	SYSTEM	ai_task_completed	ai_task	TASK-6A823244B6	{"event_id": "EVT-RT-4C9BC8A5", "snapshot_id": "SNP-RT-9BF7AB0D"}	2026-06-17T11:56:42.419427+00:00
AUD-DB4A090AF697	SYSTEM	ai_task_completed	ai_task	TASK-RT-8EE4FBF2	{"event_id": "EVT-RT-6879DCE7", "snapshot_id": "SNP-RT-413EE11C"}	2026-06-17T11:57:06.572331+00:00
AUD-9B5F7D80E8B8	SYSTEM	ai_task_completed	ai_task	TASK-AEE6E86CFC	{"event_id": "EVT-RT-C8D19DFE", "snapshot_id": "SNP-RT-42DF6B2F"}	2026-06-17T11:57:12.521896+00:00
AUD-9F83142E7A6F	SYSTEM	ai_task_completed	ai_task	TASK-RT-47072BAD	{"event_id": "EVT-RT-32E254AA", "snapshot_id": "SNP-RT-1AC59D99"}	2026-06-17T11:57:36.611190+00:00
AUD-36316213F33D	SYSTEM	ai_task_completed	ai_task	TASK-0DF92EB59A	{"event_id": "EVT-RT-75354B19", "snapshot_id": "SNP-RT-1543DA6B"}	2026-06-17T11:57:42.637768+00:00
AUD-7E3B9780E2AF	SYSTEM	ai_task_completed	ai_task	TASK-RT-1203B917	{"event_id": "EVT-RT-09453D98", "snapshot_id": "SNP-RT-6403E3EB"}	2026-06-17T11:58:06.657941+00:00
AUD-12F5410C195A	SYSTEM	ai_task_completed	ai_task	TASK-09A6337464	{"event_id": "EVT-RT-12644B29", "snapshot_id": "SNP-RT-1D62671E"}	2026-06-17T11:58:12.721783+00:00
AUD-18F2AE1A630A	SYSTEM	ai_task_completed	ai_task	TASK-RT-A738C95C	{"event_id": "EVT-RT-73569EFF", "snapshot_id": "SNP-RT-6AB8ABD1"}	2026-06-17T11:58:36.687765+00:00
AUD-90CD50176236	SYSTEM	ai_task_completed	ai_task	TASK-2120293241	{"event_id": "EVT-RT-B3DEC004", "snapshot_id": "SNP-RT-5EB604F9"}	2026-06-17T11:58:42.849766+00:00
AUD-877729138438	SYSTEM	ai_task_completed	ai_task	TASK-RT-60BDBB50	{"event_id": "EVT-RT-F0EB84F7", "snapshot_id": "SNP-RT-766AFB2E"}	2026-06-17T11:59:06.712804+00:00
AUD-8FADD6F9EC03	SYSTEM	ai_task_completed	ai_task	TASK-C3A0017CA7	{"event_id": "EVT-RT-B3F1AA01", "snapshot_id": "SNP-RT-91CEAE8E"}	2026-06-17T11:59:12.936317+00:00
AUD-2AE24510432B	SYSTEM	ai_task_completed	ai_task	TASK-RT-1EE56C84	{"event_id": "EVT-RT-0E553980", "snapshot_id": "SNP-RT-9BB69C51"}	2026-06-17T11:59:36.753823+00:00
AUD-5BDF90C1E91B	SYSTEM	ai_task_completed	ai_task	TASK-76474BF344	{"event_id": "EVT-RT-9FAF5365", "snapshot_id": "SNP-RT-EC453F34"}	2026-06-17T11:59:43.053574+00:00
AUD-B89C8F9E198C	SYSTEM	ai_task_completed	ai_task	TASK-RT-3B753493	{"event_id": "EVT-RT-4969E5D5", "snapshot_id": "SNP-RT-67C45F91"}	2026-06-17T12:00:06.780064+00:00
AUD-805A4E60224E	SYSTEM	ai_task_completed	ai_task	TASK-C981D3ED40	{"event_id": "EVT-RT-F537997C", "snapshot_id": "SNP-RT-AA2D2782"}	2026-06-17T12:00:13.173319+00:00
AUD-94F9F82A0BE2	SYSTEM	ai_task_completed	ai_task	TASK-4D261B8CD5	{"event_id": "EVT-RT-7C29A01C", "snapshot_id": "SNP-RT-DE086F0A"}	2026-06-17T12:00:43.389474+00:00
AUD-DF593C30F40D	SYSTEM	ai_task_completed	ai_task	TASK-RT-1A528527	{"event_id": "EVT-RT-7E719E1D", "snapshot_id": "SNP-RT-B7EA83A4"}	2026-06-17T12:01:07.958912+00:00
AUD-082D9548D7AD	SYSTEM	ai_task_completed	ai_task	TASK-A0F59A3F33	{"event_id": "EVT-RT-61DDB512", "snapshot_id": "SNP-RT-CECA373B"}	2026-06-17T12:01:13.489983+00:00
AUD-6365457A568E	SYSTEM	ai_task_completed	ai_task	TASK-RT-F70DFB6E	{"event_id": "EVT-RT-A4FF6D99", "snapshot_id": "SNP-RT-B4031EE2"}	2026-06-17T12:01:37.994635+00:00
AUD-D1B4FC1C3A40	SYSTEM	ai_task_completed	ai_task	TASK-1C8F0F813E	{"event_id": "EVT-RT-2A7D988A", "snapshot_id": "SNP-RT-A4CD787E"}	2026-06-17T12:01:43.579267+00:00
AUD-9BA8D1351380	SYSTEM	ai_task_completed	ai_task	TASK-RT-F813FAFE	{"event_id": "EVT-RT-C4416FC6", "snapshot_id": "SNP-RT-E4E89B8D"}	2026-06-17T12:02:08.041596+00:00
AUD-9A0ECA0B819C	SYSTEM	ai_task_completed	ai_task	TASK-D2E7BF10B9	{"event_id": "EVT-RT-CB7B7406", "snapshot_id": "SNP-RT-7B8B1DCC"}	2026-06-17T12:02:13.659210+00:00
AUD-F418EBE2AB29	SYSTEM	ai_task_completed	ai_task	TASK-RT-3C62A605	{"event_id": "EVT-RT-4BD63C4F", "snapshot_id": "SNP-RT-2B6A2078"}	2026-06-17T12:02:38.092936+00:00
AUD-419E1FD4A3D5	SYSTEM	ai_task_completed	ai_task	TASK-EB7532CE94	{"event_id": "EVT-RT-62821F91", "snapshot_id": "SNP-RT-10418E91"}	2026-06-17T12:02:43.758710+00:00
AUD-1FDB764C9B09	SYSTEM	ai_task_completed	ai_task	TASK-RT-71768B5E	{"event_id": "EVT-RT-62BE30DB", "snapshot_id": "SNP-RT-DDB7FBB0"}	2026-06-17T12:03:08.117295+00:00
AUD-FDCF45100F93	SYSTEM	ai_task_completed	ai_task	TASK-10CC0DC920	{"event_id": "EVT-RT-1FB78648", "snapshot_id": "SNP-RT-6774E4D2"}	2026-06-17T12:03:13.848368+00:00
AUD-7C057F12328F	SYSTEM	ai_task_completed	ai_task	TASK-RT-BB93A57A	{"event_id": "EVT-RT-A43EAFF5", "snapshot_id": "SNP-RT-84EC6357"}	2026-06-17T12:03:38.183599+00:00
AUD-F5448632B253	SYSTEM	ai_task_completed	ai_task	TASK-543CBBF7E4	{"event_id": "EVT-RT-05916F02", "snapshot_id": "SNP-RT-80A27F6B"}	2026-06-17T12:03:43.985593+00:00
AUD-6C077C70BF20	SYSTEM	ai_task_completed	ai_task	TASK-RT-3D46BF6D	{"event_id": "EVT-RT-6DF963D3", "snapshot_id": "SNP-RT-9148AA64"}	2026-06-17T12:04:08.218189+00:00
AUD-C1FD73C1298E	SYSTEM	ai_task_completed	ai_task	TASK-E13F48F627	{"event_id": "EVT-RT-34486E6B", "snapshot_id": "SNP-RT-4FB7AAA4"}	2026-06-17T12:04:14.101246+00:00
AUD-5AE74D592FCE	SYSTEM	ai_task_completed	ai_task	TASK-RT-B69F436A	{"event_id": "EVT-RT-F42681E4", "snapshot_id": "SNP-RT-C71AA4E6"}	2026-06-17T12:04:38.260545+00:00
AUD-757C62C74386	SYSTEM	ai_task_completed	ai_task	TASK-760A586782	{"event_id": "EVT-RT-24CC5520", "snapshot_id": "SNP-RT-4F85E516"}	2026-06-17T12:04:44.213338+00:00
AUD-719F22D32C48	SYSTEM	ai_task_completed	ai_task	TASK-RT-8E733CA8	{"event_id": "EVT-RT-C432BAC4", "snapshot_id": "SNP-RT-5D392791"}	2026-06-17T12:05:08.300024+00:00
AUD-4A1EAA49083D	SYSTEM	ai_task_completed	ai_task	TASK-9F762CF9D7	{"event_id": "EVT-RT-D66C3AD8", "snapshot_id": "SNP-RT-2A83DE7A"}	2026-06-17T12:05:14.360068+00:00
AUD-2F6E1730D8BB	SYSTEM	ai_task_completed	ai_task	TASK-RT-D6FF86D9	{"event_id": "EVT-RT-EFE0BF04", "snapshot_id": "SNP-RT-D6295644"}	2026-06-17T12:05:38.352028+00:00
AUD-35EA602F4274	SYSTEM	ai_task_completed	ai_task	TASK-6B436B10B8	{"event_id": "EVT-RT-8729A921", "snapshot_id": "SNP-RT-BE65F01F"}	2026-06-17T12:05:44.462413+00:00
AUD-EDE2B96AF570	SYSTEM	ai_task_completed	ai_task	TASK-4C5207111D	{"event_id": "EVT-RT-9749D0BE", "snapshot_id": "SNP-RT-6E913647"}	2026-06-17T12:06:14.598072+00:00
AUD-E2FE6D194E31	SYSTEM	ai_task_completed	ai_task	TASK-RT-935AFF26	{"event_id": "EVT-RT-5A24C8DB", "snapshot_id": "SNP-RT-DE0B128A"}	2026-06-17T12:06:24.017482+00:00
AUD-0764409308F3	SYSTEM	ai_task_completed	ai_task	TASK-9B354C4959	{"event_id": "EVT-RT-243EE828", "snapshot_id": "SNP-RT-7023BABC"}	2026-06-17T12:06:44.713112+00:00
AUD-FCD963560DC2	SYSTEM	ai_task_completed	ai_task	TASK-RT-355D0173	{"event_id": "EVT-RT-8B3863FE", "snapshot_id": "SNP-RT-5E9B0E93"}	2026-06-17T12:06:54.042960+00:00
AUD-3A9AFB58FF17	SYSTEM	ai_task_completed	ai_task	TASK-BF72882067	{"event_id": "EVT-RT-8E482A5F", "snapshot_id": "SNP-RT-40E7E49C"}	2026-06-17T12:07:14.811436+00:00
AUD-EF1918191D56	SYSTEM	ai_task_completed	ai_task	TASK-RT-000B5037	{"event_id": "EVT-RT-DE6A9A56", "snapshot_id": "SNP-RT-FDE691C4"}	2026-06-17T12:07:24.100361+00:00
AUD-B7D8E0750FED	SYSTEM	ai_task_completed	ai_task	TASK-7097B4AEF9	{"event_id": "EVT-RT-76DE401E", "snapshot_id": "SNP-RT-3B25D0B5"}	2026-06-17T12:07:44.920014+00:00
AUD-9AE71E690E7F	SYSTEM	ai_task_completed	ai_task	TASK-RT-F166A295	{"event_id": "EVT-RT-7B821CF5", "snapshot_id": "SNP-RT-B8038B9C"}	2026-06-17T12:07:54.118244+00:00
AUD-7871ABC1A96B	SYSTEM	ai_task_completed	ai_task	TASK-454D570E99	{"event_id": "EVT-RT-8796FD30", "snapshot_id": "SNP-RT-B1C19168"}	2026-06-17T12:08:15.001738+00:00
AUD-012691B109B8	SYSTEM	ai_task_completed	ai_task	TASK-RT-F11447E1	{"event_id": "EVT-RT-7BBF6AF3", "snapshot_id": "SNP-RT-F0E757FB"}	2026-06-17T12:08:24.153136+00:00
AUD-F73AD1112B0D	SYSTEM	ai_task_completed	ai_task	TASK-C127F91255	{"event_id": "EVT-RT-C29D2DF8", "snapshot_id": "SNP-RT-6D68CEB3"}	2026-06-17T12:08:45.094551+00:00
AUD-BE05CF4A9D25	SYSTEM	ai_task_completed	ai_task	TASK-RT-89338E26	{"event_id": "EVT-RT-E3D13E99", "snapshot_id": "SNP-RT-6263B431"}	2026-06-17T12:09:06.575753+00:00
AUD-555BF3A472C5	SYSTEM	ai_task_completed	ai_task	TASK-D6F7E28602	{"event_id": "EVT-RT-1D88100A", "snapshot_id": "SNP-RT-ADB18917"}	2026-06-17T12:09:15.206191+00:00
AUD-34964107E37C	SYSTEM	ai_task_completed	ai_task	TASK-RT-723413C9	{"event_id": "EVT-RT-A3715BA1", "snapshot_id": "SNP-RT-CCC878AA"}	2026-06-17T12:09:36.623333+00:00
AUD-B83065205365	SYSTEM	ai_task_completed	ai_task	TASK-1ED496CD26	{"event_id": "EVT-RT-706066F1", "snapshot_id": "SNP-RT-ABADABAD"}	2026-06-17T12:09:45.342930+00:00
AUD-4751CE346960	SYSTEM	ai_task_completed	ai_task	TASK-RT-2C9CC416	{"event_id": "EVT-RT-D84BF75A", "snapshot_id": "SNP-RT-0AEF0771"}	2026-06-17T12:10:06.664283+00:00
AUD-922B46FB741E	SYSTEM	ai_task_completed	ai_task	TASK-E578CD14D6	{"event_id": "EVT-RT-CE9BC831", "snapshot_id": "SNP-RT-2E015F8F"}	2026-06-17T12:10:15.426214+00:00
AUD-A6420962AF76	SYSTEM	ai_task_completed	ai_task	TASK-RT-CE102E5D	{"event_id": "EVT-RT-A7AD549E", "snapshot_id": "SNP-RT-05D8BE62"}	2026-06-17T12:10:36.716094+00:00
AUD-ED2B8CEC3327	SYSTEM	ai_task_completed	ai_task	TASK-A164F0C9C1	{"event_id": "EVT-RT-A5A077FD", "snapshot_id": "SNP-RT-DEF7CACD"}	2026-06-17T12:10:45.507897+00:00
AUD-AAB8EC595E0D	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-28470E8DF1D5	{"rule_id": "BR-ATSH-011", "rule_type": "dog_enter_gestation_barn", "object_type": "dog", "required_zone": null, "event_id": "EVT-BIO-CBFDDB69", "snapshot_id": "SNP-BIO-B9F7353C", "track_id": 802, "from_zone": "unknown", "to_zone": "gestation_barn", "zone_category": "production", "biosecurity_level": "clean", "risk_level": "high"}	2026-06-17T12:11:11.345575+00:00
AUD-56E6A3824B20	SYSTEM	workflow_violation	zone_transition	ZT-81EB05097CC3	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": ["Worker Housing", "Shower Room", "Handwash Zone", "Boot Disinfection Zone"], "attempted_step": "Production Barn", "event_id": "EVT-WF-90094FD0", "snapshot_id": "SNP-WF-9BC18D57", "track_id": 9002, "camera_id": "CAM-001", "from_zone": "worker_housing", "to_zone": "gestation_barn"}	2026-06-17T12:13:50.394885+00:00
AUD-0E751509A2FD	SYSTEM	animal_intrusion_violation	zone_transition	ZT-28470E8DF1D5	{"policy_id": "AIP-DOG", "object_type": "dog", "violation_reason": "restricted_zone_entry", "allowed_zones": ["parking_zone", "pig_loading_zone", "reception_zone"], "restricted_zones": ["farrowing_barn", "gestation_barn", "weaning_barn"], "event_id": "EVT-ANI-2E610AA6", "snapshot_id": "SNP-ANI-8D4D040B", "track_id": 802, "camera_id": "CAM-001", "from_zone": "unknown", "to_zone": "gestation_barn", "zone_category": "production", "biosecurity_level": "clean", "risk_level": "high"}	2026-06-17T12:11:11.348450+00:00
AUD-876306CBCC03	SYSTEM	animal_intrusion_violation	zone_transition	ZT-8190FD421853	{"policy_id": "AIP-CAT", "object_type": "cat", "violation_reason": "restricted_zone_entry", "allowed_zones": ["guard_house", "parking_zone", "reception_zone"], "restricted_zones": ["boar_barn", "farrowing_barn", "gestation_barn", "weaning_barn"], "event_id": "EVT-ANI-8E8AE4BC", "snapshot_id": "SNP-ANI-E189BF91", "track_id": 803, "camera_id": "CAM-001", "from_zone": "unknown", "to_zone": "farrowing_barn", "zone_category": "production", "biosecurity_level": "clean", "risk_level": "critical"}	2026-06-17T12:11:11.367387+00:00
AUD-D55EB1062776	SYSTEM	animal_intrusion_violation	zone_transition	ZT-806D5958D6CD	{"policy_id": "AIP-RAT", "object_type": "rat", "violation_reason": "restricted_zone_entry", "allowed_zones": ["parking_zone", "reception_zone"], "restricted_zones": ["feed_storage", "vet_medicine_storage"], "event_id": "EVT-ANI-BAA80749", "snapshot_id": "SNP-ANI-5B329952", "track_id": 804, "camera_id": "CAM-001", "from_zone": "unknown", "to_zone": "vet_medicine_storage", "zone_category": "storage", "biosecurity_level": "restricted", "risk_level": "high"}	2026-06-17T12:11:11.380761+00:00
AUD-EC23BFCCA9F1	SYSTEM	biosecurity_rule_violation	zone_transition	ZT-9080E9068AFE	{"rule_id": "BR-ATSH-015", "rule_type": "bird_enter_feed_storage", "object_type": "bird", "required_zone": null, "event_id": "EVT-BIO-E757CDC1", "snapshot_id": "SNP-BIO-054670C2", "track_id": 805, "from_zone": "unknown", "to_zone": "feed_storage", "zone_category": "storage", "biosecurity_level": "restricted", "risk_level": "critical"}	2026-06-17T12:11:11.394739+00:00
AUD-E0FDB5E3F7E1	SYSTEM	animal_intrusion_violation	zone_transition	ZT-9080E9068AFE	{"policy_id": "AIP-BIRD", "object_type": "bird", "violation_reason": "restricted_zone_entry", "allowed_zones": ["guard_house", "parking_zone", "reception_zone"], "restricted_zones": ["feed_storage"], "event_id": "EVT-ANI-D3386576", "snapshot_id": "SNP-ANI-113D1B1B", "track_id": 805, "camera_id": "CAM-001", "from_zone": "unknown", "to_zone": "feed_storage", "zone_category": "storage", "biosecurity_level": "restricted", "risk_level": "critical"}	2026-06-17T12:11:11.399330+00:00
AUD-0D6440FA43D8	SYSTEM	ai_task_completed	ai_task	TASK-68DE265566	{"event_id": "EVT-RT-5ED4AE33", "snapshot_id": "SNP-RT-9A19C47F"}	2026-06-17T12:11:15.575736+00:00
AUD-B4E0CB807EF5	SYSTEM	ai_task_completed	ai_task	TASK-RT-3B78F637	{"event_id": "EVT-RT-AE0AEFAB", "snapshot_id": "SNP-RT-2598F511"}	2026-06-17T12:11:35.038728+00:00
AUD-49A4FB14B0E2	SYSTEM	ai_task_completed	ai_task	TASK-EA69B69358	{"event_id": "EVT-RT-44D50ACC", "snapshot_id": "SNP-RT-515AD23A"}	2026-06-17T12:11:45.660695+00:00
AUD-278B98DA4B57	SYSTEM	ai_task_completed	ai_task	TASK-RT-C616E1F7	{"event_id": "EVT-RT-A6308519", "snapshot_id": "SNP-RT-6A2BDD13"}	2026-06-17T12:12:05.070574+00:00
AUD-44AB1FF250B2	SYSTEM	ai_task_completed	ai_task	TASK-3103ECCD11	{"event_id": "EVT-RT-C07885FD", "snapshot_id": "SNP-RT-F3A7873C"}	2026-06-17T12:12:15.811523+00:00
AUD-EF6791E141B1	SYSTEM	ai_task_completed	ai_task	TASK-RT-B76C3943	{"event_id": "EVT-RT-517512F6", "snapshot_id": "SNP-RT-15046878"}	2026-06-17T12:12:35.104002+00:00
AUD-DDD7CD893BAB	SYSTEM	ai_task_completed	ai_task	TASK-B759478131	{"event_id": "EVT-RT-68B8EF40", "snapshot_id": "SNP-RT-05E3C747"}	2026-06-17T12:12:45.926115+00:00
AUD-4ABE4FF7F540	SYSTEM	ai_task_completed	ai_task	TASK-RT-C6F62165	{"event_id": "EVT-RT-2510D1BB", "snapshot_id": "SNP-RT-0BD3F43F"}	2026-06-17T12:13:05.144236+00:00
AUD-2446D8769021	SYSTEM	ai_task_completed	ai_task	TASK-D28AD7C382	{"event_id": "EVT-RT-DCEE70A5", "snapshot_id": "SNP-RT-4C148DF3"}	2026-06-17T12:13:16.053130+00:00
AUD-D0BCAC9084C9	SYSTEM	ai_task_completed	ai_task	TASK-661E6D9D29	{"event_id": "EVT-RT-A72B8A9E", "snapshot_id": "SNP-RT-85650E0D"}	2026-06-17T12:13:46.166071+00:00
AUD-6C425CB1EF3B	SYSTEM	workflow_violation	zone_transition	ZT-947F62B3D09E	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": [], "attempted_step": "Worker Housing", "event_id": "EVT-WF-1315C3ED", "snapshot_id": "SNP-WF-D14A1ACD", "track_id": 9001, "camera_id": "CAM-001", "from_zone": "gestation_barn", "to_zone": "worker_housing"}	2026-06-17T12:13:50.257124+00:00
AUD-1E0ED4663674	SYSTEM	workflow_violation	zone_transition	ZT-4762D652F8EC	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": ["Worker Housing"], "attempted_step": "Shower Room", "event_id": "EVT-WF-060A02E4", "snapshot_id": "SNP-WF-79D8A2F2", "track_id": 9001, "camera_id": "CAM-001", "from_zone": "worker_housing", "to_zone": "shower_room"}	2026-06-17T12:13:50.286146+00:00
AUD-CBB25E329996	SYSTEM	workflow_violation	zone_transition	ZT-AAB3E366D858	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": ["Worker Housing", "Shower Room"], "attempted_step": "Handwash Zone", "event_id": "EVT-WF-ABF12928", "snapshot_id": "SNP-WF-AC262F8E", "track_id": 9001, "camera_id": "CAM-001", "from_zone": "shower_room", "to_zone": "handwash_zone"}	2026-06-17T12:13:50.303775+00:00
AUD-2B73351FB589	SYSTEM	workflow_violation	zone_transition	ZT-131B394BFD38	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": ["Worker Housing", "Shower Room", "Handwash Zone"], "attempted_step": "Boot Disinfection Zone", "event_id": "EVT-WF-CE4F72E4", "snapshot_id": "SNP-WF-9C3F6211", "track_id": 9001, "camera_id": "CAM-001", "from_zone": "handwash_zone", "to_zone": "boot_disinfection_tray"}	2026-06-17T12:13:50.324326+00:00
AUD-9857114C31C8	SYSTEM	workflow_violation	zone_transition	ZT-91FE0CB48834	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": ["Worker Housing", "Shower Room", "Handwash Zone", "Boot Disinfection Zone"], "attempted_step": "Production Barn", "event_id": "EVT-WF-901C5E5D", "snapshot_id": "SNP-WF-26CFB324", "track_id": 9001, "camera_id": "CAM-001", "from_zone": "boot_disinfection_tray", "to_zone": "gestation_barn"}	2026-06-17T12:13:50.348647+00:00
AUD-1379003DCE56	SYSTEM	workflow_violation	zone_transition	ZT-24882CA094BB	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": [], "attempted_step": "Worker Housing", "event_id": "EVT-WF-A48D488C", "snapshot_id": "SNP-WF-C03B3606", "track_id": 9002, "camera_id": "CAM-001", "from_zone": "gestation_barn", "to_zone": "worker_housing"}	2026-06-17T12:13:50.371166+00:00
AUD-F59C7C76E228	SYSTEM	ai_task_completed	ai_task	TASK-RT-C94A94A7	{"event_id": "EVT-RT-CC593150", "snapshot_id": "SNP-RT-9A15179F"}	2026-06-17T12:13:56.000653+00:00
AUD-3ADD2D50E6E7	SYSTEM	ai_task_completed	ai_task	TASK-E16BEEE4E7	{"event_id": "EVT-RT-9B4225A4", "snapshot_id": "SNP-RT-AFD51829"}	2026-06-17T12:14:16.368286+00:00
AUD-B38F0884E9FB	SYSTEM	workflow_violation	zone_transition	ZT-4C57A27D064E	{"workflow_id": "WF-PERSON-ENTRY", "workflow_name": "Person Entry to Production", "skipped_steps": ["Shower Room", "Handwash Zone", "Boot Disinfection Zone"], "attempted_step": "Production Barn", "event_id": "EVT-WF-1F0BBB7A", "snapshot_id": "SNP-WF-5A8F2F54", "track_id": 9102, "camera_id": "CAM-001", "from_zone": "worker_housing", "to_zone": "gestation_barn"}	2026-06-17T12:14:22.227415+00:00
AUD-5041974537B6	SYSTEM	ai_task_completed	ai_task	TASK-RT-4EC72A21	{"event_id": "EVT-RT-5350A703", "snapshot_id": "SNP-RT-240125A2"}	2026-06-17T12:14:44.992399+00:00
AUD-A2E230681A21	SYSTEM	ai_task_completed	ai_task	TASK-49E998584A	{"event_id": "EVT-RT-BB25B9E5", "snapshot_id": "SNP-RT-48EA74B5"}	2026-06-17T12:14:46.489520+00:00
AUD-AD943C24BCDA	SYSTEM	ai_task_completed	ai_task	TASK-RT-AEA38A6C	{"event_id": "EVT-RT-E4B62A01", "snapshot_id": "SNP-RT-193D72E0"}	2026-06-17T12:15:15.044499+00:00
AUD-A462824E2A78	SYSTEM	ai_task_completed	ai_task	TASK-AEC2DCE7D8	{"event_id": "EVT-RT-77610B8A", "snapshot_id": "SNP-RT-D41F84E2"}	2026-06-17T12:15:16.604814+00:00
AUD-5C8AD5A21E1B	SYSTEM	ai_task_completed	ai_task	TASK-RT-A0137723	{"event_id": "EVT-RT-042A8A0D", "snapshot_id": "SNP-RT-5EC0E120"}	2026-06-17T12:15:45.087559+00:00
AUD-0333B668C7F0	SYSTEM	ai_task_completed	ai_task	TASK-F24E0A7B7C	{"event_id": "EVT-RT-9D5BA740", "snapshot_id": "SNP-RT-BDCF167C"}	2026-06-17T12:15:46.770802+00:00
AUD-706649503E0D	SYSTEM	ai_task_completed	ai_task	TASK-RT-1C11EF49	{"event_id": "EVT-RT-FAED45DF", "snapshot_id": "SNP-RT-670D2B6D"}	2026-06-17T12:16:15.123680+00:00
AUD-EBB7038C0DFB	SYSTEM	ai_task_completed	ai_task	TASK-F9B9354DCF	{"event_id": "EVT-RT-9A978146", "snapshot_id": "SNP-RT-8B978266"}	2026-06-17T12:16:16.868707+00:00
AUD-89E4684A8116	SYSTEM	ai_task_completed	ai_task	TASK-E008B4B54D	{"event_id": "EVT-RT-40DAA38E", "snapshot_id": "SNP-RT-0E8C884D"}	2026-06-17T12:16:47.104131+00:00
AUD-6CDCB0A3D664	SYSTEM	ai_task_completed	ai_task	TASK-RT-6120B8EA	{"event_id": "EVT-RT-55DA9BE2", "snapshot_id": "SNP-RT-DBC8CD8A"}	2026-06-17T12:16:50.747767+00:00
AUD-DE33D1ADA646	SYSTEM	ai_task_completed	ai_task	TASK-5BB1298B27	{"event_id": "EVT-RT-A717A77F", "snapshot_id": "SNP-RT-C78C0A26"}	2026-06-17T12:17:17.294177+00:00
AUD-C880C0ACC66E	SYSTEM	ai_task_completed	ai_task	TASK-RT-E3C35065	{"event_id": "EVT-RT-0916AD15", "snapshot_id": "SNP-RT-B9F6412B"}	2026-06-17T12:17:20.812932+00:00
AUD-C933D1EEC570	SYSTEM	ai_task_completed	ai_task	TASK-4797842EC8	{"event_id": "EVT-RT-75071576", "snapshot_id": "SNP-RT-A14EE8FF"}	2026-06-17T12:17:47.465147+00:00
AUD-BB5E04835704	SYSTEM	ai_task_completed	ai_task	TASK-RT-AAA0F4E6	{"event_id": "EVT-RT-94B22A2A", "snapshot_id": "SNP-RT-6C749B98"}	2026-06-17T12:17:50.855788+00:00
AUD-599116155147	SYSTEM	ai_task_completed	ai_task	TASK-04703C2BB1	{"event_id": "EVT-RT-39B46F37", "snapshot_id": "SNP-RT-417F3646"}	2026-06-17T12:18:17.570870+00:00
AUD-2217F8AE87C4	SYSTEM	ai_task_completed	ai_task	TASK-RT-893D0F62	{"event_id": "EVT-RT-08214CFB", "snapshot_id": "SNP-RT-F10B31AB"}	2026-06-17T12:18:20.924866+00:00
AUD-FB798F705EDE	SYSTEM	ai_task_completed	ai_task	TASK-F167BDBB9F	{"event_id": "EVT-RT-38636402", "snapshot_id": "SNP-RT-0F2E261A"}	2026-06-17T12:18:47.748696+00:00
AUD-2223AEBBF3F2	SYSTEM	ai_task_completed	ai_task	TASK-RT-37A72AAC	{"event_id": "EVT-RT-2F54AE18", "snapshot_id": "SNP-RT-F4C08919"}	2026-06-17T12:18:50.982149+00:00
AUD-40A6F5CDE0B2	SYSTEM	ai_task_completed	ai_task	TASK-5FE8023728	{"event_id": "EVT-RT-1FC284BC", "snapshot_id": "SNP-RT-3F469AE8"}	2026-06-17T12:19:14.869931+00:00
AUD-D21DFEA5B5EF	SYSTEM	ai_task_completed	ai_task	TASK-RT-D0203B23	{"event_id": "EVT-RT-87D7DE14", "snapshot_id": "SNP-RT-02E43133"}	2026-06-17T12:19:36.813334+00:00
AUD-9BFA893414B5	SYSTEM	ai_task_completed	ai_task	TASK-E0423E19ED	{"event_id": "EVT-RT-E7614EB2", "snapshot_id": "SNP-RT-5A2C50D2"}	2026-06-17T12:19:45.040777+00:00
AUD-1C40B725E600	SYSTEM	ai_task_completed	ai_task	TASK-RT-EF73A8CF	{"event_id": "EVT-RT-E19C7F8C", "snapshot_id": "SNP-RT-18B8A1C4"}	2026-06-17T12:20:06.902136+00:00
AUD-1622E15CE80C	SYSTEM	ai_task_completed	ai_task	TASK-22FDB91698	{"event_id": "EVT-RT-8979345E", "snapshot_id": "SNP-RT-BD789764"}	2026-06-17T12:20:15.202679+00:00
AUD-0BCD158FCB93	SYSTEM	ai_task_completed	ai_task	TASK-RT-223B1B1F	{"event_id": "EVT-RT-03BCC394", "snapshot_id": "SNP-RT-2C1DEEB6"}	2026-06-17T12:20:36.982563+00:00
AUD-8E39F07B7614	SYSTEM	ai_task_completed	ai_task	TASK-650CFBF240	{"event_id": "EVT-RT-B83DE6C6", "snapshot_id": "SNP-RT-6E34ED11"}	2026-06-17T12:20:45.319250+00:00
AUD-2396F65ED269	SYSTEM	ai_task_completed	ai_task	TASK-RT-EFB3EB00	{"event_id": "EVT-RT-DCAAA0E8", "snapshot_id": "SNP-RT-ABA0945E"}	2026-06-17T12:21:07.083395+00:00
AUD-B5B7DD3B8FE8	SYSTEM	ai_task_completed	ai_task	TASK-838DB40551	{"event_id": "EVT-RT-9C41953C", "snapshot_id": "SNP-RT-B23D2A13"}	2026-06-17T12:21:15.483177+00:00
AUD-BEBDB13EB1C7	SYSTEM	ai_task_completed	ai_task	TASK-RT-78B7CD17	{"event_id": "EVT-RT-F33336E4", "snapshot_id": "SNP-RT-4F9BA590"}	2026-06-17T12:21:37.192591+00:00
AUD-FB9E68D1F8A1	SYSTEM	ai_task_completed	ai_task	TASK-57AF279C5D	{"event_id": "EVT-RT-302AF9C6", "snapshot_id": "SNP-RT-562C786F"}	2026-06-17T12:21:45.643736+00:00
AUD-582D5B1D5A72	SYSTEM	ai_task_completed	ai_task	TASK-RT-2F60EE66	{"event_id": "EVT-RT-490A521E", "snapshot_id": "SNP-RT-71E8DD15"}	2026-06-17T12:22:07.272729+00:00
AUD-7375844ADD13	SYSTEM	ai_task_completed	ai_task	TASK-BC76773EE9	{"event_id": "EVT-RT-3888C83A", "snapshot_id": "SNP-RT-1D967C89"}	2026-06-17T12:22:15.763710+00:00
AUD-E356358B31B9	SYSTEM	ai_task_completed	ai_task	TASK-RT-5C423D46	{"event_id": "EVT-RT-D0240B0E", "snapshot_id": "SNP-RT-246CB529"}	2026-06-17T12:22:37.636102+00:00
AUD-F66E553B4A6E	SYSTEM	ai_task_completed	ai_task	TASK-66202D1188	{"event_id": "EVT-RT-BCB0A674", "snapshot_id": "SNP-RT-FFEC3A8D"}	2026-06-17T12:22:45.920871+00:00
AUD-F22813D8659E	SYSTEM	ai_task_completed	ai_task	TASK-RT-610DAC9B	{"event_id": "EVT-RT-7B15E743", "snapshot_id": "SNP-RT-93CB87E5"}	2026-06-17T12:23:07.719745+00:00
AUD-F6923812D173	SYSTEM	ai_task_completed	ai_task	TASK-764609B39B	{"event_id": "EVT-RT-DAD18EA0", "snapshot_id": "SNP-RT-B919AB63"}	2026-06-17T12:23:16.098411+00:00
AUD-510928B9BB13	SYSTEM	ai_task_completed	ai_task	TASK-RT-6BB7F5DB	{"event_id": "EVT-RT-AD545480", "snapshot_id": "SNP-RT-3B0E4993"}	2026-06-17T12:23:37.787641+00:00
AUD-9C973BD95977	SYSTEM	ai_task_completed	ai_task	TASK-5F8E541790	{"event_id": "EVT-RT-83008B4F", "snapshot_id": "SNP-RT-C4CED4C3"}	2026-06-17T12:23:46.256822+00:00
AUD-33515538FA91	SYSTEM	ai_task_completed	ai_task	TASK-RT-2E7E75F0	{"event_id": "EVT-RT-47559862", "snapshot_id": "SNP-RT-C55F6D20"}	2026-06-17T12:24:07.874291+00:00
AUD-0DABBBCD6AC8	SYSTEM	ai_task_completed	ai_task	TASK-00818B2C61	{"event_id": "EVT-RT-9357836D", "snapshot_id": "SNP-RT-AF4737CC"}	2026-06-17T12:24:16.426130+00:00
AUD-DD9AC4BB7D8D	SYSTEM	ai_task_completed	ai_task	TASK-RT-48B59829	{"event_id": "EVT-RT-3F574785", "snapshot_id": "SNP-RT-5BD65339"}	2026-06-17T12:24:37.960334+00:00
AUD-3EC77E17A6E1	SYSTEM	ai_task_completed	ai_task	TASK-68A3EB2724	{"event_id": "EVT-RT-127F1B8A", "snapshot_id": "SNP-RT-160894A0"}	2026-06-17T12:24:46.714438+00:00
AUD-6674B82E5162	SYSTEM	ai_task_completed	ai_task	TASK-RT-288B29A8	{"event_id": "EVT-RT-B9ABB01A", "snapshot_id": "SNP-RT-65772B6F"}	2026-06-17T12:25:12.981564+00:00
AUD-C696B4A2AD61	SYSTEM	ai_task_completed	ai_task	TASK-F5D8ACF6C3	{"event_id": "EVT-RT-D96B147C", "snapshot_id": "SNP-RT-6C2A8C3D"}	2026-06-17T12:25:16.854062+00:00
AUD-C042E321BEC0	SYSTEM	ai_task_completed	ai_task	TASK-A93310DFFC	{"event_id": "EVT-RT-1E205229", "snapshot_id": "SNP-RT-ABBEDE36"}	2026-06-17T12:26:47.241431+00:00
AUD-F123510B8019	SYSTEM	ai_task_completed	ai_task	TASK-RT-787BB4A1	{"event_id": "EVT-RT-4AF32614", "snapshot_id": "SNP-RT-80C867B3"}	2026-06-17T12:27:01.859342+00:00
AUD-6D42EF6F968E	SYSTEM	ai_task_completed	ai_task	TASK-DA96D2776E	{"event_id": "EVT-RT-0E46F8A8", "snapshot_id": "SNP-RT-1E60CCE1"}	2026-06-17T12:27:17.441574+00:00
AUD-DC5978CD17B2	SYSTEM	ai_task_completed	ai_task	TASK-RT-BA136EF2	{"event_id": "EVT-RT-874D74CE", "snapshot_id": "SNP-RT-04E114DE"}	2026-06-17T12:27:31.933242+00:00
AUD-BD6628C476C3	SYSTEM	ai_task_completed	ai_task	TASK-576965C687	{"event_id": "EVT-RT-1E1FCD3E", "snapshot_id": "SNP-RT-C295C72C"}	2026-06-17T12:27:47.579301+00:00
AUD-F006D48369E6	SYSTEM	ai_task_completed	ai_task	TASK-RT-2331C849	{"event_id": "EVT-RT-CE79CE0A", "snapshot_id": "SNP-RT-E2D924F9"}	2026-06-17T12:28:02.021888+00:00
AUD-671D7706963D	SYSTEM	ai_task_completed	ai_task	TASK-768C0C5E9A	{"event_id": "EVT-RT-C95A8A0E", "snapshot_id": "SNP-RT-AA3F1CFA"}	2026-06-17T12:28:17.721540+00:00
AUD-BF5FE68424B9	SYSTEM	ai_task_completed	ai_task	TASK-RT-7BCCF284	{"event_id": "EVT-RT-7534788E", "snapshot_id": "SNP-RT-D4AB3A26"}	2026-06-17T12:28:32.108925+00:00
AUD-FCD304021D52	SYSTEM	ai_task_completed	ai_task	TASK-A5D479433B	{"event_id": "EVT-RT-1747DCB2", "snapshot_id": "SNP-RT-CD24C6D4"}	2026-06-17T12:28:47.883168+00:00
AUD-049B7D5A3D27	SYSTEM	ai_task_completed	ai_task	TASK-RT-A0800A67	{"event_id": "EVT-RT-920B3643", "snapshot_id": "SNP-RT-B01A5DDB"}	2026-06-17T12:29:02.187733+00:00
AUD-B0E194C1FAD2	SYSTEM	ai_task_completed	ai_task	TASK-81AF32E84F	{"event_id": "EVT-RT-52277007", "snapshot_id": "SNP-RT-F9DBEE35"}	2026-06-17T12:29:48.184650+00:00
AUD-B5E2C4B84109	SYSTEM	ai_task_completed	ai_task	TASK-RT-8854EDA1	{"event_id": "EVT-RT-1F91C61C", "snapshot_id": "SNP-RT-FF5F1EF4"}	2026-06-17T12:30:10.896384+00:00
AUD-BC5E39595E0C	SYSTEM	ai_task_completed	ai_task	TASK-713E4072BA	{"event_id": "EVT-RT-040AC757", "snapshot_id": "SNP-RT-8F578E54"}	2026-06-17T12:30:18.364008+00:00
AUD-A7CB51C06244	SYSTEM	ai_task_completed	ai_task	TASK-RT-1F505D62	{"event_id": "EVT-RT-DC672173", "snapshot_id": "SNP-RT-F321E0EA"}	2026-06-17T12:30:40.970291+00:00
AUD-B7B93165BE56	SYSTEM	ai_task_completed	ai_task	TASK-DC67CD8EB5	{"event_id": "EVT-RT-E3F74136", "snapshot_id": "SNP-RT-8CE7777E"}	2026-06-17T12:30:48.496403+00:00
AUD-C633C7E8B2A5	SYSTEM	ai_task_completed	ai_task	TASK-RT-F08BB091	{"event_id": "EVT-RT-EE1C72FC", "snapshot_id": "SNP-RT-E8D18471"}	2026-06-17T12:31:11.055758+00:00
AUD-6160F5D3EED6	SYSTEM	ai_task_completed	ai_task	TASK-23D5A34786	{"event_id": "EVT-RT-465C5378", "snapshot_id": "SNP-RT-8B1182F2"}	2026-06-17T12:31:18.630473+00:00
AUD-4FE455B1DF9D	SYSTEM	ai_task_completed	ai_task	TASK-RT-F0976D26	{"event_id": "EVT-RT-0DC24FD7", "snapshot_id": "SNP-RT-2DE616B5"}	2026-06-17T12:31:41.122471+00:00
AUD-8A2C4DAF1C79	SYSTEM	ai_task_completed	ai_task	TASK-703E7A0AFF	{"event_id": "EVT-RT-06BAB461", "snapshot_id": "SNP-RT-DA095CBB"}	2026-06-17T12:31:48.789421+00:00
AUD-1FE0F678D50B	SYSTEM	ai_task_completed	ai_task	TASK-RT-84A2694A	{"event_id": "EVT-RT-B011B8CD", "snapshot_id": "SNP-RT-BF3A7C4C"}	2026-06-17T12:32:11.204072+00:00
AUD-098038DC5C78	SYSTEM	ai_task_completed	ai_task	TASK-17662BEBAA	{"event_id": "EVT-RT-BB297A1E", "snapshot_id": "SNP-RT-198E0B82"}	2026-06-17T12:32:18.942121+00:00
AUD-A73EFED212E4	SYSTEM	ai_task_completed	ai_task	TASK-RT-F5302C6E	{"event_id": "EVT-RT-1DB45716", "snapshot_id": "SNP-RT-51528A55"}	2026-06-17T12:32:41.277560+00:00
AUD-3AD5F3A568FC	SYSTEM	ai_task_completed	ai_task	TASK-0080693F24	{"event_id": "EVT-RT-6DBF0A6F", "snapshot_id": "SNP-RT-26915CBD"}	2026-06-17T12:32:49.084378+00:00
AUD-D06C6E6CFF3E	SYSTEM	ai_task_completed	ai_task	TASK-RT-7BFE9769	{"event_id": "EVT-RT-4B10B881", "snapshot_id": "SNP-RT-715949C3"}	2026-06-17T12:33:11.332369+00:00
AUD-57892D2944EA	SYSTEM	ai_task_completed	ai_task	TASK-E221CC2E69	{"event_id": "EVT-RT-80FD7557", "snapshot_id": "SNP-RT-9B70ED5A"}	2026-06-17T12:33:19.217437+00:00
AUD-B2981BF00E5F	SYSTEM	ai_task_completed	ai_task	TASK-RT-0749546A	{"event_id": "EVT-RT-06B42C62", "snapshot_id": "SNP-RT-2B5A8E23"}	2026-06-17T12:33:41.409853+00:00
AUD-7D1EA40168FA	SYSTEM	ai_task_completed	ai_task	TASK-C2BCCDB9CE	{"event_id": "EVT-RT-1C90AA58", "snapshot_id": "SNP-RT-BBC987B8"}	2026-06-17T12:33:49.335597+00:00
AUD-50EA6E2FAFC0	SYSTEM	ai_task_completed	ai_task	TASK-RT-85A37A93	{"event_id": "EVT-RT-952C9BAB", "snapshot_id": "SNP-RT-E276C81F"}	2026-06-17T12:34:11.484530+00:00
AUD-9A58072B1891	SYSTEM	ai_task_completed	ai_task	TASK-2CA397F905	{"event_id": "EVT-RT-F90EE8A7", "snapshot_id": "SNP-RT-B641868B"}	2026-06-17T12:34:19.509184+00:00
AUD-FB19889FCA80	SYSTEM	ai_task_completed	ai_task	TASK-RT-96BE581A	{"event_id": "EVT-RT-50800B4C", "snapshot_id": "SNP-RT-F5CC7600"}	2026-06-17T12:34:41.550642+00:00
AUD-2397FF8F8FC2	SYSTEM	ai_task_completed	ai_task	TASK-ED85F54E50	{"event_id": "EVT-RT-F9E18578", "snapshot_id": "SNP-RT-0318AE89"}	2026-06-17T12:34:49.640759+00:00
AUD-37A69126E34E	SYSTEM	ai_task_completed	ai_task	TASK-RT-105C3D6E	{"event_id": "EVT-RT-07E9DDB7", "snapshot_id": "SNP-RT-248EBFAB"}	2026-06-17T12:35:11.616481+00:00
AUD-F136E6D464A2	SYSTEM	ai_task_completed	ai_task	TASK-3E4E9D8087	{"event_id": "EVT-RT-8A91E029", "snapshot_id": "SNP-RT-F6C1B06B"}	2026-06-17T12:35:19.821870+00:00
AUD-4CA9B3580161	SYSTEM	workflow_violation	zone_transition	ZT-6135C34A1C89	{"workflow_id": "WF-GESTATION-ENTRY", "workflow_name": "Vào chuồng nái", "violation_code": "KHONG_TAM_SAT_TRUNG", "skipped_steps": ["Nhà tắm", "Sát trùng tay", "Sát trùng ủng"], "attempted_step": "Chuồng nái", "event_id": "EVT-WF-537A8BDE", "snapshot_id": "SNP-WF-47912C95", "track_id": 1002, "camera_id": "CAM-001", "from_zone": "worker_housing", "to_zone": "gestation_barn"}	2026-06-17T12:35:29.932766+00:00
AUD-CD49A944F8D7	SYSTEM	workflow_violation	zone_transition	ZT-6135C34A1C89	{"workflow_id": "WF-GESTATION-ENTRY", "workflow_name": "Vào chuồng nái", "violation_code": "KHONG_SAT_TRUNG_TAY", "skipped_steps": ["Nhà tắm", "Sát trùng tay", "Sát trùng ủng"], "attempted_step": "Chuồng nái", "event_id": "EVT-WF-96887688", "snapshot_id": "SNP-WF-48B65CF9", "track_id": 1002, "camera_id": "CAM-001", "from_zone": "worker_housing", "to_zone": "gestation_barn"}	2026-06-17T12:35:29.957599+00:00
AUD-352C8BE1634D	SYSTEM	workflow_violation	zone_transition	ZT-6135C34A1C89	{"workflow_id": "WF-GESTATION-ENTRY", "workflow_name": "Vào chuồng nái", "violation_code": "KHONG_SAT_TRUNG_UNG", "skipped_steps": ["Nhà tắm", "Sát trùng tay", "Sát trùng ủng"], "attempted_step": "Chuồng nái", "event_id": "EVT-WF-5E79B1D8", "snapshot_id": "SNP-WF-004D4659", "track_id": 1002, "camera_id": "CAM-001", "from_zone": "worker_housing", "to_zone": "gestation_barn"}	2026-06-17T12:35:29.981880+00:00
AUD-75EA8048709B	SYSTEM	workflow_violation	zone_transition	ZT-CDC09FA915D9	{"workflow_id": "WF-GESTATION-ENTRY", "workflow_name": "Vào chuồng nái", "violation_code": "KHONG_SAT_TRUNG_TAY", "skipped_steps": ["Sát trùng tay", "Sát trùng ủng"], "attempted_step": "Chuồng nái", "event_id": "EVT-WF-F300E318", "snapshot_id": "SNP-WF-48DC4564", "track_id": 1003, "camera_id": "CAM-001", "from_zone": "boot_disinfection_tray", "to_zone": "gestation_barn"}	2026-06-17T12:35:30.144320+00:00
AUD-794FCDE9C407	SYSTEM	workflow_violation	zone_transition	ZT-CDC09FA915D9	{"workflow_id": "WF-GESTATION-ENTRY", "workflow_name": "Vào chuồng nái", "violation_code": "KHONG_SAT_TRUNG_UNG", "skipped_steps": ["Sát trùng tay", "Sát trùng ủng"], "attempted_step": "Chuồng nái", "event_id": "EVT-WF-E7EE8297", "snapshot_id": "SNP-WF-EA58827D", "track_id": 1003, "camera_id": "CAM-001", "from_zone": "boot_disinfection_tray", "to_zone": "gestation_barn"}	2026-06-17T12:35:30.178057+00:00
AUD-973D2BF9B10C	SYSTEM	workflow_violation	zone_transition	ZT-5088E40C3624	{"workflow_id": "WF-GESTATION-ENTRY", "workflow_name": "Vào chuồng nái", "violation_code": "KHONG_SAT_TRUNG_UNG", "skipped_steps": ["Sát trùng ủng"], "attempted_step": "Chuồng nái", "event_id": "EVT-WF-867C066E", "snapshot_id": "SNP-WF-993758FC", "track_id": 1004, "camera_id": "CAM-001", "from_zone": "handwash_zone", "to_zone": "gestation_barn"}	2026-06-17T12:35:30.320766+00:00
AUD-C10396251453	SYSTEM	ai_task_completed	ai_task	TASK-CE9685B498	{"event_id": "EVT-RT-300E78E2", "snapshot_id": "SNP-RT-4B898F6F"}	2026-06-17T12:36:20.039352+00:00
AUD-37802DBA0076	SYSTEM	ai_task_completed	ai_task	TASK-RT-2C974F37	{"event_id": "EVT-RT-B9365C23", "snapshot_id": "SNP-RT-91876A2E"}	2026-06-17T12:36:34.354092+00:00
AUD-BC63694CC4CA	SYSTEM	ai_task_completed	ai_task	TASK-F6DE67EB32	{"event_id": "EVT-RT-51561BA6", "snapshot_id": "SNP-RT-8EC37D73"}	2026-06-17T12:36:50.172606+00:00
AUD-4C6E0DD1A38D	SYSTEM	ai_task_completed	ai_task	TASK-RT-406F06B5	{"event_id": "EVT-RT-2F8E7668", "snapshot_id": "SNP-RT-07A7F427"}	2026-06-17T12:37:04.448195+00:00
AUD-50E001EE5159	SYSTEM	ai_task_completed	ai_task	TASK-24496E2062	{"event_id": "EVT-RT-2EA3206A", "snapshot_id": "SNP-RT-0F554227"}	2026-06-17T12:37:20.354623+00:00
AUD-C1906C3484AE	SYSTEM	ai_task_completed	ai_task	TASK-RT-26AF4E21	{"event_id": "EVT-RT-0A9227A3", "snapshot_id": "SNP-RT-BC5538D3"}	2026-06-17T12:37:34.521686+00:00
AUD-A69E4AB0DDE9	SYSTEM	ai_task_completed	ai_task	TASK-A5028A92F9	{"event_id": "EVT-RT-A8071FB6", "snapshot_id": "SNP-RT-78987922"}	2026-06-17T12:37:50.516070+00:00
AUD-703E98C689B8	SYSTEM	ai_task_completed	ai_task	TASK-RT-1991EF94	{"event_id": "EVT-RT-A7A24170", "snapshot_id": "SNP-RT-B44D2725"}	2026-06-17T12:38:04.610875+00:00
AUD-05F3F59F1325	SYSTEM	ai_task_completed	ai_task	TASK-200A21CE4E	{"event_id": "EVT-RT-D7D28C77", "snapshot_id": "SNP-RT-252C3D4D"}	2026-06-17T12:38:20.683181+00:00
AUD-AED08152B9AB	SYSTEM	ai_task_completed	ai_task	TASK-RT-6EAB69C4	{"event_id": "EVT-RT-0F04704E", "snapshot_id": "SNP-RT-CD12D571"}	2026-06-17T12:38:34.675451+00:00
AUD-9E36BD214E71	SYSTEM	ai_task_completed	ai_task	TASK-DD811CB648	{"event_id": "EVT-RT-9AA0D6C5", "snapshot_id": "SNP-RT-5DF42562"}	2026-06-17T12:38:50.820226+00:00
AUD-84571E5A4352	SYSTEM	ai_task_completed	ai_task	TASK-RT-045DBF7C	{"event_id": "EVT-RT-F765A692", "snapshot_id": "SNP-RT-E94920F2"}	2026-06-17T12:39:04.758786+00:00
AUD-77C1130503FF	SYSTEM	ai_task_completed	ai_task	TASK-FD9A08EADD	{"event_id": "EVT-RT-24285AB9", "snapshot_id": "SNP-RT-DF7E13E1"}	2026-06-17T12:39:21.016809+00:00
AUD-0D554871DB6C	SYSTEM	ai_task_completed	ai_task	TASK-RT-8CB70F1C	{"event_id": "EVT-RT-4805F23E", "snapshot_id": "SNP-RT-479B8A2E"}	2026-06-17T12:39:34.851051+00:00
AUD-F5262B24AFAF	SYSTEM	ai_task_completed	ai_task	TASK-74E1AE3998	{"event_id": "EVT-RT-E13E7CB9", "snapshot_id": "SNP-RT-8C0A141F"}	2026-06-17T12:39:51.203022+00:00
AUD-E3A234ACBF8B	SYSTEM	ai_task_completed	ai_task	TASK-RT-7980DB36	{"event_id": "EVT-RT-D77F7CC8", "snapshot_id": "SNP-RT-218ABC82"}	2026-06-17T12:40:04.934979+00:00
AUD-57E220493A5A	SYSTEM	ai_task_completed	ai_task	TASK-CB7081A358	{"event_id": "EVT-RT-02801074", "snapshot_id": "SNP-RT-6D2981AD"}	2026-06-17T12:40:21.386309+00:00
AUD-C5DF6458219F	SYSTEM	ai_task_completed	ai_task	TASK-RT-3591CCD9	{"event_id": "EVT-RT-AAE0629F", "snapshot_id": "SNP-RT-18952AC7"}	2026-06-17T12:40:35.012580+00:00
AUD-A16E765D12E4	SYSTEM	ai_task_completed	ai_task	TASK-4081ADFB35	{"event_id": "EVT-RT-2E09042E", "snapshot_id": "SNP-RT-0580D3C2"}	2026-06-17T12:40:51.541208+00:00
AUD-BC04AEA035EC	SYSTEM	ai_task_completed	ai_task	TASK-RT-662F0C1F	{"event_id": "EVT-RT-58CD44C6", "snapshot_id": "SNP-RT-16F09FD7"}	2026-06-17T12:41:05.101959+00:00
AUD-0A279CA6A611	SYSTEM	ai_task_completed	ai_task	TASK-594BE019BE	{"event_id": "EVT-RT-CBB3FD58", "snapshot_id": "SNP-RT-35328ED6"}	2026-06-17T12:41:21.720871+00:00
AUD-EFC3CBF96854	SYSTEM	ai_task_completed	ai_task	TASK-RT-E68CB28A	{"event_id": "EVT-RT-649921F1", "snapshot_id": "SNP-RT-C9355CE7"}	2026-06-17T12:41:35.202547+00:00
AUD-8F214DBFFD10	SYSTEM	ai_task_completed	ai_task	TASK-02A98BB514	{"event_id": "EVT-RT-20F6A442", "snapshot_id": "SNP-RT-AFD8A312"}	2026-06-17T12:41:51.911397+00:00
AUD-6D3274725778	SYSTEM	ai_task_completed	ai_task	TASK-RT-7748E39E	{"event_id": "EVT-RT-78D7F067", "snapshot_id": "SNP-RT-4FFF0942"}	2026-06-17T12:42:05.284038+00:00
AUD-9E621DE52A71	SYSTEM	ai_task_completed	ai_task	TASK-BAE0F2DBF9	{"event_id": "EVT-RT-00E443C2", "snapshot_id": "SNP-RT-C8FA4E04"}	2026-06-17T12:42:22.102040+00:00
AUD-08045582E68E	SYSTEM	ai_task_completed	ai_task	TASK-RT-C4E162C8	{"event_id": "EVT-RT-44E2C2AE", "snapshot_id": "SNP-RT-8AE51310"}	2026-06-17T12:42:35.380460+00:00
\.


--
-- Data for Name: biosecurity_rules; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.biosecurity_rules (id, severity, enabled, object_type, from_zone, to_zone, required_zone, rule_code, rule_name_vi, rule_name_en, category, description, created_at) FROM stdin;
BR-ATSH-013	high	t	cat	any_zone	boar_barn	\N	CAT_ENTER_BOAR_BARN	Cat enter boar barn	Cat enter boar barn	animal	Cat enter boar barn	2026-06-17T00:00:00+07:00
BR-ATSH-001	critical	t	person	parking_zone	gestation_barn	person_disinfection_zone	PERSON_PARKING_TO_GESTATION_WITHOUT_DISINFECTION	Person parking to gestation barn without person disinfection	Person parking to gestation barn without person disinfection	human	Person parking to gestation barn without person disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-002	critical	t	person	reception_zone	farrowing_barn	person_disinfection_zone	PERSON_RECEPTION_TO_FARROWING_WITHOUT_DISINFECTION	Person reception to farrowing barn without person disinfection	Person reception to farrowing barn without person disinfection	human	Person reception to farrowing barn without person disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-003	critical	t	person	worker_housing	boar_barn	shower_room	PERSON_WORKER_HOUSING_TO_BOAR_WITHOUT_SHOWER	Person worker housing to boar barn without shower	Person worker housing to boar barn without shower	human	Person worker housing to boar barn without shower	2026-06-17T00:00:00+07:00
BR-ATSH-004	critical	t	person	guard_house	weaning_barn	person_disinfection_zone	PERSON_GUARD_TO_WEANING_WITHOUT_DISINFECTION	Person guard house to weaning barn without person disinfection	Person guard house to weaning barn without person disinfection	human	Person guard house to weaning barn without person disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-005	critical	t	person	cafeteria	fattening_barn	person_disinfection_zone	PERSON_CAFETERIA_TO_FATTENING_WITHOUT_DISINFECTION	Person cafeteria to fattening barn without person disinfection	Person cafeteria to fattening barn without person disinfection	human	Person cafeteria to fattening barn without person disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-006	high	t	person	pig_loading_zone	quarantine_barn	boot_disinfection_tray	PERSON_LOADING_TO_QUARANTINE_WITHOUT_BOOT_TRAY	Person pig loading to quarantine barn without boot disinfection	Person pig loading to quarantine barn without boot disinfection	human	Person pig loading to quarantine barn without boot disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-007	critical	t	person	quarantine_barn	gestation_barn	person_disinfection_zone	PERSON_QUARANTINE_TO_GESTATION_WITHOUT_DISINFECTION	Person quarantine barn to gestation barn without person disinfection	Person quarantine barn to gestation barn without person disinfection	human	Person quarantine barn to gestation barn without person disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-011	critical	t	dog	any_zone	gestation_barn	\N	DOG_ENTER_GESTATION_BARN	Dog enter gestation barn	Dog enter gestation barn	animal	Dog enter gestation barn	2026-06-17T00:00:00+07:00
BR-ATSH-008	critical	t	vehicle	parking_zone	pig_loading_zone	vehicle_disinfection_zone	VEHICLE_PARKING_TO_LOADING_WITHOUT_DISINFECTION	Vehicle parking to pig loading without vehicle disinfection	Vehicle parking to pig loading without vehicle disinfection	vehicle	Vehicle parking to pig loading without vehicle disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-009	critical	t	vehicle	parking_zone	gestation_barn	vehicle_disinfection_zone	VEHICLE_PARKING_TO_GESTATION_WITHOUT_DISINFECTION	Vehicle parking to gestation barn without vehicle disinfection	Vehicle parking to gestation barn without vehicle disinfection	vehicle	Vehicle parking to gestation barn without vehicle disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-010	high	t	vehicle	reception_zone	pig_loading_zone	vehicle_disinfection_zone	VEHICLE_RECEPTION_TO_LOADING_WITHOUT_DISINFECTION	Vehicle reception to pig loading without vehicle disinfection	Vehicle reception to pig loading without vehicle disinfection	vehicle	Vehicle reception to pig loading without vehicle disinfection	2026-06-17T00:00:00+07:00
BR-ATSH-012	critical	t	dog	any_zone	farrowing_barn	\N	DOG_ENTER_FARROWING_BARN	Dog enter farrowing barn	Dog enter farrowing barn	animal	Dog enter farrowing barn	2026-06-17T00:00:00+07:00
BR-ATSH-014	high	t	cat	any_zone	weaning_barn	\N	CAT_ENTER_WEANING_BARN	Cat enter weaning barn	Cat enter weaning barn	animal	Cat enter weaning barn	2026-06-17T00:00:00+07:00
BR-ATSH-015	warning	t	bird	any_zone	feed_storage	\N	BIRD_ENTER_FEED_STORAGE	Bird enter feed storage	Bird enter feed storage	animal	Bird enter feed storage	2026-06-17T00:00:00+07:00
BR-ATSH-016	warning	t	bird	any_zone	vet_medicine_storage	\N	BIRD_ENTER_VET_MEDICINE_STORAGE	Bird enter vet medicine storage	Bird enter vet medicine storage	animal	Bird enter vet medicine storage	2026-06-17T00:00:00+07:00
BR-EF058651	critical	t	person	dirty_zone	safe_zone	disinfection_zone	PERSON_DIRTY_ZONE_TO_SAFE_ZONE_WITHOUT_DISINFECTION_ZONE	Person Dirty Zone to Safe Zone without Disinfection Zone	Person Dirty Zone to Safe Zone without Disinfection Zone	human	Person Dirty Zone to Safe Zone without Disinfection Zone	2026-06-17T00:00:00+07:00
BR-VN-001	critical	t	catalog	\N	\N	\N	PERSON_RESTRICTED_ZONE	Người xâm nhập vùng cấm	Person enters restricted zone	human	Phát hiện người đi vào khu vực ATSH bị hạn chế hoặc cấm tuyệt đối.	2026-06-17T00:00:00+07:00
BR-VN-002	critical	t	catalog	\N	\N	\N	PERSON_QUARANTINE_INTRUSION	Người xâm nhập khu cách ly	Person enters quarantine zone	human	Phát hiện người xâm nhập khu cách ly trái quy định.	2026-06-17T00:00:00+07:00
BR-VN-003	critical	t	catalog	\N	\N	\N	ANIMAL_INTRUSION_DOG	Chó xâm nhập khu chăn nuôi	Dog enters production area	animal	Phát hiện chó xâm nhập khu chuồng heo hoặc khu sản xuất.	2026-06-17T00:00:00+07:00
BR-VN-004	high	t	catalog	\N	\N	\N	ANIMAL_INTRUSION_CAT	Mèo xâm nhập khu chăn nuôi	Cat enters production area	animal	Phát hiện mèo xâm nhập khu chuồng heo hoặc khu sản xuất.	2026-06-17T00:00:00+07:00
BR-VN-005	critical	t	catalog	\N	\N	\N	ANIMAL_INTRUSION_RAT	Chuột xuất hiện trong khu vực sản xuất	Rat detected in production area	animal	Phát hiện chuột trong khu vực sản xuất.	2026-06-17T00:00:00+07:00
BR-VN-006	medium	t	catalog	\N	\N	\N	ANIMAL_INTRUSION_BIRD	Chim xuất hiện trong kho cám	Bird detected in feed storage	animal	Phát hiện chim trong kho cám hoặc khu thức ăn.	2026-06-17T00:00:00+07:00
BR-VN-007	critical	t	catalog	\N	\N	\N	SKIP_SHOWER	Không tắm sát trùng	Skipped mandatory shower	human	Công nhân bỏ qua bước tắm sát trùng trước khi vào khu sạch.	2026-06-17T00:00:00+07:00
BR-VN-008	critical	t	catalog	\N	\N	\N	SKIP_HAND_DISINFECTION	Không sát trùng tay	Skipped hand disinfection	human	Công nhân không thực hiện sát trùng tay tại khu rửa tay.	2026-06-17T00:00:00+07:00
BR-VN-009	critical	t	catalog	\N	\N	\N	SKIP_BOOT_DISINFECTION	Không sát trùng ủng	Skipped boot disinfection	human	Công nhân bỏ qua khay sát trùng ủng trước khi vào khu sản xuất.	2026-06-17T00:00:00+07:00
BR-VN-010	high	t	catalog	\N	\N	\N	NO_BOOTS	Không mang ủng bảo hộ	Missing protective boots	human	Phát hiện người không mang ủng bảo hộ trong khu ATSH.	2026-06-17T00:00:00+07:00
BR-VN-011	medium	t	catalog	\N	\N	\N	WRONG_UNIFORM_COLOR	Sai màu quần áo bảo hộ	Wrong protective uniform color	human	Phát hiện công nhân mặc sai màu quần áo so với khu vực được phép.	2026-06-17T00:00:00+07:00
BR-VN-012	critical	t	catalog	\N	\N	\N	DIRTY_TO_CLEAN	Di chuyển từ vùng bẩn sang vùng sạch	Dirty zone to clean zone movement	movement	Phát hiện di chuyển trực tiếp từ khu bẩn sang khu sạch mà không qua quy trình ATSH.	2026-06-17T00:00:00+07:00
BR-VN-013	high	t	catalog	\N	\N	\N	VISITOR_CONTACT_WORKER	Công nhân tiếp xúc người ngoài	Worker contacts external visitor	contact	Phát hiện công nhân tiếp xúc trực tiếp với người ngoài trong khu trại.	2026-06-17T00:00:00+07:00
BR-VN-014	high	t	catalog	\N	\N	\N	DRIVER_CONTACT_WORKER	Công nhân tiếp xúc lái xe	Worker contacts vehicle driver	contact	Phát hiện công nhân tiếp xúc trực tiếp với lái xe tại khu vực ATSH.	2026-06-17T00:00:00+07:00
BR-VN-015	critical	t	catalog	\N	\N	\N	VEHICLE_NO_DISINFECTION	Xe chưa sát trùng	Vehicle without disinfection	vehicle	Phát hiện xe vào khu trại mà chưa qua khu sát trùng xe.	2026-06-17T00:00:00+07:00
BR-VN-016	high	t	catalog	\N	\N	\N	VEHICLE_SHORT_DISINFECTION	Xe sát trùng không đủ thời gian	Vehicle disinfection time too short	vehicle	Phát hiện xe rời khu sát trùng trước thời gian quy định.	2026-06-17T00:00:00+07:00
BR-VN-017	medium	t	catalog	\N	\N	\N	VEHICLE_WRONG_PARKING	Xe đỗ sai vị trí	Vehicle parked in wrong area	vehicle	Phát hiện xe đỗ ngoài vị trí quy định trong khu trại.	2026-06-17T00:00:00+07:00
BR-VN-018	high	t	catalog	\N	\N	\N	FEED_TRUCK_WRONG_ZONE	Xe chở cám vào sai khu vực	Feed truck enters wrong zone	vehicle	Phát hiện xe chở cám vào sai khu vực quy định.	2026-06-17T00:00:00+07:00
BR-VN-019	critical	t	catalog	\N	\N	\N	PIG_RETURN_TO_BARN	Heo từ khu xuất bán quay lại khu nuôi	Pig returns from loading to barn	pig	Phát hiện heo quay lại khu nuôi sau khi đã vào khu xuất bán.	2026-06-17T00:00:00+07:00
BR-VN-020	critical	t	catalog	\N	\N	\N	BOAR_BARN_INTRUSION	Xâm nhập khu đực giống	Unauthorized boar barn entry	movement	Phát hiện xâm nhập khu đực giống trái quy trình ATSH.	2026-06-17T00:00:00+07:00
BR-VN-021	critical	t	catalog	\N	\N	\N	FARROWING_BARN_INTRUSION	Xâm nhập khu nái đẻ	Unauthorized farrowing barn entry	movement	Phát hiện xâm nhập khu nái đẻ trái quy trình ATSH.	2026-06-17T00:00:00+07:00
BR-VN-022	critical	t	catalog	\N	\N	\N	GESTATION_BARN_INTRUSION	Xâm nhập khu nái bầu	Unauthorized gestation barn entry	movement	Phát hiện xâm nhập khu nái bầu trái quy trình ATSH.	2026-06-17T00:00:00+07:00
BR-VN-023	critical	t	catalog	\N	\N	\N	WEANING_BARN_INTRUSION	Xâm nhập khu cai sữa	Unauthorized weaning barn entry	movement	Phát hiện xâm nhập khu cai sữa trái quy trình ATSH.	2026-06-17T00:00:00+07:00
BR-VN-024	critical	t	catalog	\N	\N	\N	FATTENING_BARN_INTRUSION	Xâm nhập khu heo thịt	Unauthorized fattening barn entry	movement	Phát hiện xâm nhập khu heo thịt trái quy trình ATSH.	2026-06-17T00:00:00+07:00
BR-VN-025	critical	t	catalog	\N	\N	\N	VET_MEDICINE_STORAGE_INTRUSION	Xâm nhập kho thuốc	Unauthorized vet medicine storage entry	movement	Phát hiện xâm nhập kho thuốc trái quy định.	2026-06-17T00:00:00+07:00
BR-VN-026	high	t	catalog	\N	\N	\N	SUPPLY_STORAGE_INTRUSION	Xâm nhập kho vật tư	Unauthorized supply storage entry	movement	Phát hiện xâm nhập kho vật tư trái quy định.	2026-06-17T00:00:00+07:00
BR-VN-027	critical	t	catalog	\N	\N	\N	FEED_STORAGE_INTRUSION	Xâm nhập kho cám	Unauthorized feed storage entry	movement	Phát hiện xâm nhập kho cám trái quy định.	2026-06-17T00:00:00+07:00
\.


--
-- Data for Name: camera_health; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.camera_health (id, farm_id, camera_id, fps, bitrate, last_seen, status) FROM stdin;
HLT-001	FARM-001	CAM-001	30	4.2	2026-06-17T17:10:00+07:00	healthy
HLT-002	FARM-001	CAM-002	25	6.8	2026-06-17T17:10:00+07:00	healthy
HLT-003	FARM-001	CAM-003	25	4.2	2026-06-17T17:10:00+07:00	healthy
HLT-004	FARM-001	CAM-004	24	4.2	2026-06-17T17:10:00+07:00	healthy
HLT-005	FARM-001	CAM-005	0	4.2	2026-06-17T17:10:00+07:00	offline
HLT-006	FARM-002	CAM-006	20	2.6	2026-06-17T17:10:00+07:00	healthy
HLT-007	FARM-002	CAM-007	24	4.2	2026-06-17T17:10:00+07:00	healthy
HLT-008	FARM-002	CAM-008	25	4.2	2026-06-17T17:10:00+07:00	healthy
HLT-009	FARM-002	CAM-009	20	2.6	2026-06-17T17:10:00+07:00	healthy
\.


--
-- Data for Name: camera_streams; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.camera_streams (id, camera_id, rtsp_url, fps, resolution, stream_status) FROM stdin;
STR-001	CAM-001	rtsp://ams:demo@192.168.10.11:554/live	30	1080p	live
STR-002	CAM-002	rtsp://ams:demo@192.168.10.12:554/live	25	2K	live
STR-003	CAM-003	rtsp://ams:demo@192.168.10.13:554/live	25	1080p	live
STR-004	CAM-004	rtsp://ams:demo@192.168.10.14:554/live	24	1080p	live
STR-005	CAM-005	rtsp://ams:demo@192.168.10.15:554/live	0	1080p	offline
STR-006	CAM-006	rtsp://ams:demo@192.168.10.16:554/live	20	720p	live
STR-007	CAM-007	rtsp://ams:demo@192.168.10.17:554/live	24	1080p	live
STR-008	CAM-008	rtsp://ams:demo@192.168.10.18:554/live	25	1080p	live
STR-009	CAM-009	rtsp://ams:demo@192.168.10.19:554/live	20	720p	live
\.


--
-- Data for Name: cameras; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.cameras (id, name, zone, ip_address, status, resolution, uptime, fps, is_active, farm_id) FROM stdin;
CAM-001	Camera Cổng trại	Cổng trại	192.168.10.11	online	1080p	99.8	30	t	FARM-001
CAM-002	Camera Khu nái 01	Khu nái	192.168.10.12	online	2K	99.3	25	t	FARM-001
CAM-003	Camera Khu nái 02	Khu nái	192.168.10.13	online	1080p	98.7	25	t	FARM-001
CAM-004	Camera Khu đực giống	Khu đực giống	192.168.10.14	online	1080p	97.9	24	t	FARM-001
CAM-005	Camera Khu cách ly	Khu cách ly	192.168.10.15	offline	1080p	82.1	0	t	FARM-001
CAM-006	Camera Hành lang chính	Hành lang chính	192.168.10.16	online	720p	99.1	20	t	FARM-002
CAM-007	Camera Khu con	Khu con	192.168.10.17	online	1080p	98.4	24	t	FARM-002
CAM-008	Camera Kho thức ăn	Kho thức ăn	192.168.10.18	online	1080p	99.6	25	t	FARM-002
CAM-009	Camera Bể xử lý nước	Xử lý nước	192.168.10.19	online	720p	96.5	20	t	FARM-002
\.


--
-- Data for Name: edge_devices; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.edge_devices (id, farm_id, device_name, device_type, serial_number, status, assigned_cameras) FROM stdin;
EDGE-001	FARM-001	AI Box Cổng trại	NVIDIA Jetson Orin	AMS-EDGE-001	online	5
EDGE-002	FARM-002	AI Box Khu chuồng	NVIDIA Jetson Xavier	AMS-EDGE-002	online	4
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.employees (id, employee_code, full_name, department, assigned_zone, uniform_color, face_image, active) FROM stdin;
EMP-002	NV-002	Trần Thị Bình	Sản xuất	farrowing_barn	xanh lá		t
EMP-003	NV-003	Lê Hoàng Cường	An ninh	guard_house	xám		t
EMP-004	NV-004	Phạm Minh Dũng	Thú y	vet_medicine_storage	trắng		t
EMP-005	NV-005	Võ Thị Em	Kho vận	feed_storage	cam		t
EMP-006	NV-006	Hoàng Văn Phúc	Hành chính	reception_zone	xanh dương		t
EMP-007	NV-007	Đặng Thị Giang	Sản xuất	weaning_barn	xanh lá		t
EMP-008	NV-008	Bùi Quốc Huy	Sản xuất	boar_barn	xanh lá		f
EMP-582761A9	NV-TEST	Test Nhan Vien	Kho vận	fattening_barn	xanh lá		t
EMP-001	NV-001	Nguyễn Văn An	Sản xuất	gestation_barn	xanh lá		t
\.


--
-- Data for Name: event_snapshots; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.event_snapshots (id, event_id, image_path, thumbnail_path) FROM stdin;
SNP-001	EVT-001	/storage/snapshots/EVT-001.jpg	/storage/snapshots/thumbs/EVT-001.jpg
SNP-002	EVT-002	/storage/snapshots/EVT-002.jpg	/storage/snapshots/thumbs/EVT-002.jpg
SNP-003	EVT-003	/storage/snapshots/EVT-003.jpg	/storage/snapshots/thumbs/EVT-003.jpg
SNP-004	EVT-004	/storage/snapshots/EVT-004.jpg	/storage/snapshots/thumbs/EVT-004.jpg
SNP-005	EVT-005	/storage/snapshots/EVT-005.jpg	/storage/snapshots/thumbs/EVT-005.jpg
SNP-006	EVT-006	/storage/snapshots/EVT-006.jpg	/storage/snapshots/thumbs/EVT-006.jpg
SNP-007	EVT-007	/storage/snapshots/EVT-007.jpg	/storage/snapshots/thumbs/EVT-007.jpg
SNP-008	EVT-008	/storage/snapshots/EVT-008.jpg	/storage/snapshots/thumbs/EVT-008.jpg
SNP-009	EVT-009	/storage/snapshots/EVT-009.jpg	/storage/snapshots/thumbs/EVT-009.jpg
SNP-010	EVT-010	/storage/snapshots/EVT-010.jpg	/storage/snapshots/thumbs/EVT-010.jpg
SNP-011	EVT-011	/storage/snapshots/EVT-011.jpg	/storage/snapshots/thumbs/EVT-011.jpg
SNP-012	EVT-012	/storage/snapshots/EVT-012.jpg	/storage/snapshots/thumbs/EVT-012.jpg
SNP-013	EVT-013	/storage/snapshots/EVT-013.jpg	/storage/snapshots/thumbs/EVT-013.jpg
SNP-014	EVT-014	/storage/snapshots/EVT-014.jpg	/storage/snapshots/thumbs/EVT-014.jpg
SNP-015	EVT-015	/storage/snapshots/EVT-015.jpg	/storage/snapshots/thumbs/EVT-015.jpg
SNP-016	EVT-016	/storage/snapshots/EVT-016.jpg	/storage/snapshots/thumbs/EVT-016.jpg
SNP-017	EVT-017	/storage/snapshots/EVT-017.jpg	/storage/snapshots/thumbs/EVT-017.jpg
SNP-018	EVT-018	/storage/snapshots/EVT-018.jpg	/storage/snapshots/thumbs/EVT-018.jpg
SNP-019	EVT-019	/storage/snapshots/EVT-019.jpg	/storage/snapshots/thumbs/EVT-019.jpg
SNP-020	EVT-020	/storage/snapshots/EVT-020.jpg	/storage/snapshots/thumbs/EVT-020.jpg
SNP-RT-E18F89D8	EVT-RT-BFC14B09	/storage/runtime/EVT-RT-BFC14B09.jpg	/storage/runtime/thumbs/EVT-RT-BFC14B09.jpg
SNP-RT-0DB16962	EVT-RT-ABAB9E7D	/storage/runtime/EVT-RT-ABAB9E7D.jpg	/storage/runtime/thumbs/EVT-RT-ABAB9E7D.jpg
SNP-RT-50F07727	EVT-RT-6BB404E1	/storage/runtime/EVT-RT-6BB404E1.jpg	/storage/runtime/thumbs/EVT-RT-6BB404E1.jpg
SNP-RT-833A090A	EVT-RT-9599DF0C	/storage/runtime/EVT-RT-9599DF0C.jpg	/storage/runtime/thumbs/EVT-RT-9599DF0C.jpg
SNP-RT-677B91EC	EVT-RT-E338BA34	/storage/runtime/EVT-RT-E338BA34.jpg	/storage/runtime/thumbs/EVT-RT-E338BA34.jpg
SNP-RT-C4A7AF0F	EVT-RT-70D6A36E	/storage/runtime/EVT-RT-70D6A36E.jpg	/storage/runtime/thumbs/EVT-RT-70D6A36E.jpg
SNP-RT-1B431BAA	EVT-RT-A5AD8924	/storage/runtime/EVT-RT-A5AD8924.jpg	/storage/runtime/thumbs/EVT-RT-A5AD8924.jpg
SNP-RT-39E7F534	EVT-RT-9277B021	/storage/runtime/EVT-RT-9277B021.jpg	/storage/runtime/thumbs/EVT-RT-9277B021.jpg
SNP-RT-39BFF036	EVT-RT-9A030D8C	/storage/runtime/EVT-RT-9A030D8C.jpg	/storage/runtime/thumbs/EVT-RT-9A030D8C.jpg
SNP-RT-35CAFBC6	EVT-RT-34FB34CF	/storage/runtime/EVT-RT-34FB34CF.jpg	/storage/runtime/thumbs/EVT-RT-34FB34CF.jpg
SNP-RT-1487B010	EVT-RT-C46862AA	/storage/runtime/EVT-RT-C46862AA.jpg	/storage/runtime/thumbs/EVT-RT-C46862AA.jpg
SNP-RT-F6F3D5D2	EVT-RT-927CC36B	/storage/runtime/EVT-RT-927CC36B.jpg	/storage/runtime/thumbs/EVT-RT-927CC36B.jpg
SNP-RT-7F2A5C87	EVT-RT-876895A2	/storage/runtime/EVT-RT-876895A2.jpg	/storage/runtime/thumbs/EVT-RT-876895A2.jpg
SNP-RT-B7F0A587	EVT-RT-2D922793	/storage/runtime/EVT-RT-2D922793.jpg	/storage/runtime/thumbs/EVT-RT-2D922793.jpg
SNP-RT-FB84D30A	EVT-RT-C423F422	/storage/runtime/EVT-RT-C423F422.jpg	/storage/runtime/thumbs/EVT-RT-C423F422.jpg
SNP-RT-22114E02	EVT-RT-DE295378	/storage/runtime/EVT-RT-DE295378.jpg	/storage/runtime/thumbs/EVT-RT-DE295378.jpg
SNP-RT-1A7DB589	EVT-RT-02F7DF6A	/storage/runtime/EVT-RT-02F7DF6A.jpg	/storage/runtime/thumbs/EVT-RT-02F7DF6A.jpg
SNP-RT-01668253	EVT-RT-E3500358	/storage/runtime/EVT-RT-E3500358.jpg	/storage/runtime/thumbs/EVT-RT-E3500358.jpg
SNP-RT-4756FC06	EVT-RT-08DE7C83	/storage/runtime/EVT-RT-08DE7C83.jpg	/storage/runtime/thumbs/EVT-RT-08DE7C83.jpg
SNP-RT-B9953C15	EVT-RT-17B29287	/storage/runtime/EVT-RT-17B29287.jpg	/storage/runtime/thumbs/EVT-RT-17B29287.jpg
SNP-RT-B7D73998	EVT-RT-81276D8F	/storage/runtime/EVT-RT-81276D8F.jpg	/storage/runtime/thumbs/EVT-RT-81276D8F.jpg
SNP-RT-4488BA09	EVT-RT-CEC94A75	/storage/runtime/EVT-RT-CEC94A75.jpg	/storage/runtime/thumbs/EVT-RT-CEC94A75.jpg
SNP-RT-0F14A9B3	EVT-RT-3D1B30D7	/storage/runtime/EVT-RT-3D1B30D7.jpg	/storage/runtime/thumbs/EVT-RT-3D1B30D7.jpg
SNP-RT-AEDC5B77	EVT-RT-BAE6E1D7	/storage/runtime/EVT-RT-BAE6E1D7.jpg	/storage/runtime/thumbs/EVT-RT-BAE6E1D7.jpg
SNP-RT-FB3141A1	EVT-RT-84A7C1CC	/storage/runtime/EVT-RT-84A7C1CC.jpg	/storage/runtime/thumbs/EVT-RT-84A7C1CC.jpg
SNP-RT-BEBF895E	EVT-RT-8E95A8E7	/storage/runtime/EVT-RT-8E95A8E7.jpg	/storage/runtime/thumbs/EVT-RT-8E95A8E7.jpg
SNP-RT-E191AF81	EVT-RT-9BD213BC	/storage/runtime/EVT-RT-9BD213BC.jpg	/storage/runtime/thumbs/EVT-RT-9BD213BC.jpg
SNP-RT-9126DA26	EVT-RT-6D08308D	/storage/runtime/EVT-RT-6D08308D.jpg	/storage/runtime/thumbs/EVT-RT-6D08308D.jpg
SNP-RT-48B03081	EVT-RT-D466ABAC	/storage/runtime/EVT-RT-D466ABAC.jpg	/storage/runtime/thumbs/EVT-RT-D466ABAC.jpg
SNP-RT-CB8F77E0	EVT-RT-AC0705AD	/storage/runtime/EVT-RT-AC0705AD.jpg	/storage/runtime/thumbs/EVT-RT-AC0705AD.jpg
SNP-RT-CC6A91DE	EVT-RT-915DA336	/storage/runtime/EVT-RT-915DA336.jpg	/storage/runtime/thumbs/EVT-RT-915DA336.jpg
SNP-RT-4EB86ACB	EVT-RT-6B65B8F0	/storage/runtime/EVT-RT-6B65B8F0.jpg	/storage/runtime/thumbs/EVT-RT-6B65B8F0.jpg
SNP-RT-9309CD64	EVT-RT-BD626578	/storage/runtime/EVT-RT-BD626578.jpg	/storage/runtime/thumbs/EVT-RT-BD626578.jpg
SNP-RT-0D3DE2B0	EVT-RT-BE27BDC6	/storage/runtime/EVT-RT-BE27BDC6.jpg	/storage/runtime/thumbs/EVT-RT-BE27BDC6.jpg
SNP-RT-7B782F3D	EVT-RT-73006EA4	/storage/runtime/EVT-RT-73006EA4.jpg	/storage/runtime/thumbs/EVT-RT-73006EA4.jpg
SNP-RT-51D2EB19	EVT-RT-A480BC66	/storage/runtime/EVT-RT-A480BC66.jpg	/storage/runtime/thumbs/EVT-RT-A480BC66.jpg
SNP-RT-5513A9A8	EVT-RT-6A2EEA15	/storage/runtime/EVT-RT-6A2EEA15.jpg	/storage/runtime/thumbs/EVT-RT-6A2EEA15.jpg
SNP-RT-2701EAEE	EVT-RT-7A471A36	/storage/runtime/EVT-RT-7A471A36.jpg	/storage/runtime/thumbs/EVT-RT-7A471A36.jpg
SNP-RT-F9D2AA67	EVT-RT-A578B0E9	/storage/runtime/EVT-RT-A578B0E9.jpg	/storage/runtime/thumbs/EVT-RT-A578B0E9.jpg
SNP-RT-747E79C9	EVT-RT-9FF2F5FA	/storage/runtime/EVT-RT-9FF2F5FA.jpg	/storage/runtime/thumbs/EVT-RT-9FF2F5FA.jpg
SNP-RT-2582CCFD	EVT-RT-D1863B4B	/storage/runtime/EVT-RT-D1863B4B.jpg	/storage/runtime/thumbs/EVT-RT-D1863B4B.jpg
SNP-RT-DC9FF292	EVT-RT-F0842F88	/storage/runtime/EVT-RT-F0842F88.jpg	/storage/runtime/thumbs/EVT-RT-F0842F88.jpg
SNP-RT-92486101	EVT-RT-DF66D38B	/storage/runtime/EVT-RT-DF66D38B.jpg	/storage/runtime/thumbs/EVT-RT-DF66D38B.jpg
SNP-RT-09A4C2B0	EVT-RT-7C31CBAF	/storage/runtime/EVT-RT-7C31CBAF.jpg	/storage/runtime/thumbs/EVT-RT-7C31CBAF.jpg
SNP-RT-E03AD713	EVT-RT-5BCE2E00	/storage/runtime/EVT-RT-5BCE2E00.jpg	/storage/runtime/thumbs/EVT-RT-5BCE2E00.jpg
SNP-RT-3574621F	EVT-RT-D193DAD9	/storage/runtime/EVT-RT-D193DAD9.jpg	/storage/runtime/thumbs/EVT-RT-D193DAD9.jpg
SNP-RT-E27ED637	EVT-RT-B8FA3700	/storage/runtime/EVT-RT-B8FA3700.jpg	/storage/runtime/thumbs/EVT-RT-B8FA3700.jpg
SNP-RT-A58976C4	EVT-RT-21536871	/storage/runtime/EVT-RT-21536871.jpg	/storage/runtime/thumbs/EVT-RT-21536871.jpg
SNP-RT-B6E85CBE	EVT-RT-FA3F75F4	/storage/runtime/EVT-RT-FA3F75F4.jpg	/storage/runtime/thumbs/EVT-RT-FA3F75F4.jpg
SNP-RT-C8FA1717	EVT-RT-CC39D3BF	/storage/runtime/EVT-RT-CC39D3BF.jpg	/storage/runtime/thumbs/EVT-RT-CC39D3BF.jpg
SNP-RT-D7AC0941	EVT-RT-8FC08AB1	/storage/runtime/EVT-RT-8FC08AB1.jpg	/storage/runtime/thumbs/EVT-RT-8FC08AB1.jpg
SNP-RT-D6FB9A5A	EVT-RT-6496304B	/storage/runtime/EVT-RT-6496304B.jpg	/storage/runtime/thumbs/EVT-RT-6496304B.jpg
SNP-RT-D6CB3AEC	EVT-RT-58C22B56	/storage/runtime/EVT-RT-58C22B56.jpg	/storage/runtime/thumbs/EVT-RT-58C22B56.jpg
SNP-RT-32C3A2C8	EVT-RT-8C2CD6F7	/storage/runtime/EVT-RT-8C2CD6F7.jpg	/storage/runtime/thumbs/EVT-RT-8C2CD6F7.jpg
SNP-RT-1D0507D0	EVT-RT-34B0B646	/storage/runtime/EVT-RT-34B0B646.jpg	/storage/runtime/thumbs/EVT-RT-34B0B646.jpg
SNP-RT-834A4752	EVT-RT-FAE1F3A6	/storage/runtime/EVT-RT-FAE1F3A6.jpg	/storage/runtime/thumbs/EVT-RT-FAE1F3A6.jpg
SNP-RT-C7D6E2BB	EVT-RT-E5959412	/storage/runtime/EVT-RT-E5959412.jpg	/storage/runtime/thumbs/EVT-RT-E5959412.jpg
SNP-RT-D0CCD12E	EVT-RT-189AD3CF	/storage/runtime/EVT-RT-189AD3CF.jpg	/storage/runtime/thumbs/EVT-RT-189AD3CF.jpg
SNP-RT-0BCB4AE0	EVT-RT-15B5B56B	/storage/runtime/EVT-RT-15B5B56B.jpg	/storage/runtime/thumbs/EVT-RT-15B5B56B.jpg
SNP-RT-352D8782	EVT-RT-62048F22	/storage/runtime/EVT-RT-62048F22.jpg	/storage/runtime/thumbs/EVT-RT-62048F22.jpg
SNP-RT-66B53F41	EVT-RT-B2331059	/storage/runtime/EVT-RT-B2331059.jpg	/storage/runtime/thumbs/EVT-RT-B2331059.jpg
SNP-RT-01EA45B8	EVT-RT-A58C4061	/storage/runtime/EVT-RT-A58C4061.jpg	/storage/runtime/thumbs/EVT-RT-A58C4061.jpg
SNP-RT-5ACBBE93	EVT-RT-21821EFE	/storage/runtime/EVT-RT-21821EFE.jpg	/storage/runtime/thumbs/EVT-RT-21821EFE.jpg
SNP-RT-50AB5946	EVT-RT-EAFE0103	/storage/runtime/EVT-RT-EAFE0103.jpg	/storage/runtime/thumbs/EVT-RT-EAFE0103.jpg
SNP-RT-E92EA25B	EVT-RT-3CD59E0A	/storage/runtime/EVT-RT-3CD59E0A.jpg	/storage/runtime/thumbs/EVT-RT-3CD59E0A.jpg
SNP-RT-AF7ADE53	EVT-RT-8CB0CFDE	/storage/runtime/EVT-RT-8CB0CFDE.jpg	/storage/runtime/thumbs/EVT-RT-8CB0CFDE.jpg
SNP-RT-07CB56D7	EVT-RT-035FC18A	/storage/runtime/EVT-RT-035FC18A.jpg	/storage/runtime/thumbs/EVT-RT-035FC18A.jpg
SNP-RT-C9EE7BC5	EVT-RT-8B98E8F6	/storage/runtime/EVT-RT-8B98E8F6.jpg	/storage/runtime/thumbs/EVT-RT-8B98E8F6.jpg
SNP-RT-13331A81	EVT-RT-A62E7420	/storage/runtime/EVT-RT-A62E7420.jpg	/storage/runtime/thumbs/EVT-RT-A62E7420.jpg
SNP-RT-879620AA	EVT-RT-890B4B35	/storage/runtime/EVT-RT-890B4B35.jpg	/storage/runtime/thumbs/EVT-RT-890B4B35.jpg
SNP-RT-78760BA7	EVT-RT-BD7B3FFD	/storage/runtime/EVT-RT-BD7B3FFD.jpg	/storage/runtime/thumbs/EVT-RT-BD7B3FFD.jpg
SNP-RT-138DE4A2	EVT-RT-4C51ED30	/storage/runtime/EVT-RT-4C51ED30.jpg	/storage/runtime/thumbs/EVT-RT-4C51ED30.jpg
SNP-RT-7DDF2F33	EVT-RT-F76AD84A	/storage/runtime/EVT-RT-F76AD84A.jpg	/storage/runtime/thumbs/EVT-RT-F76AD84A.jpg
SNP-RT-42507479	EVT-RT-0528AC11	/storage/runtime/EVT-RT-0528AC11.jpg	/storage/runtime/thumbs/EVT-RT-0528AC11.jpg
SNP-RT-AD367C46	EVT-RT-AB639D38	/storage/runtime/EVT-RT-AB639D38.jpg	/storage/runtime/thumbs/EVT-RT-AB639D38.jpg
SNP-RT-047502A6	EVT-RT-01B855E7	/storage/runtime/EVT-RT-01B855E7.jpg	/storage/runtime/thumbs/EVT-RT-01B855E7.jpg
SNP-RT-33E3E69C	EVT-RT-D11FA1B5	/storage/runtime/EVT-RT-D11FA1B5.jpg	/storage/runtime/thumbs/EVT-RT-D11FA1B5.jpg
SNP-RT-8125A032	EVT-RT-BDD8026A	/storage/runtime/EVT-RT-BDD8026A.jpg	/storage/runtime/thumbs/EVT-RT-BDD8026A.jpg
SNP-RT-82A17860	EVT-RT-7E9F006D	/storage/runtime/EVT-RT-7E9F006D.jpg	/storage/runtime/thumbs/EVT-RT-7E9F006D.jpg
SNP-RT-6DA590DF	EVT-RT-9B32B69A	/storage/runtime/EVT-RT-9B32B69A.jpg	/storage/runtime/thumbs/EVT-RT-9B32B69A.jpg
SNP-RT-9BBC7994	EVT-RT-7ACE6473	/storage/runtime/EVT-RT-7ACE6473.jpg	/storage/runtime/thumbs/EVT-RT-7ACE6473.jpg
SNP-RT-C97B3054	EVT-RT-D5061419	/storage/runtime/EVT-RT-D5061419.jpg	/storage/runtime/thumbs/EVT-RT-D5061419.jpg
SNP-RT-11CBB77D	EVT-RT-1ABFE50B	/storage/runtime/EVT-RT-1ABFE50B.jpg	/storage/runtime/thumbs/EVT-RT-1ABFE50B.jpg
SNP-RT-43FE1A39	EVT-RT-4C60F9CC	/storage/runtime/EVT-RT-4C60F9CC.jpg	/storage/runtime/thumbs/EVT-RT-4C60F9CC.jpg
SNP-RT-16AC0BD0	EVT-RT-F7C36D50	/storage/runtime/EVT-RT-F7C36D50.jpg	/storage/runtime/thumbs/EVT-RT-F7C36D50.jpg
SNP-RT-C3614D82	EVT-RT-666372AF	/storage/runtime/EVT-RT-666372AF.jpg	/storage/runtime/thumbs/EVT-RT-666372AF.jpg
SNP-RT-F6C034B1	EVT-RT-F190C297	/storage/runtime/EVT-RT-F190C297.jpg	/storage/runtime/thumbs/EVT-RT-F190C297.jpg
SNP-RT-B1053058	EVT-RT-8B9E19CA	/storage/runtime/EVT-RT-8B9E19CA.jpg	/storage/runtime/thumbs/EVT-RT-8B9E19CA.jpg
SNP-RT-301B1892	EVT-RT-8928E2BF	/storage/runtime/EVT-RT-8928E2BF.jpg	/storage/runtime/thumbs/EVT-RT-8928E2BF.jpg
SNP-RT-9BA6FB50	EVT-RT-1E3F177D	/storage/runtime/EVT-RT-1E3F177D.jpg	/storage/runtime/thumbs/EVT-RT-1E3F177D.jpg
SNP-RT-78798827	EVT-RT-742BC921	/storage/runtime/EVT-RT-742BC921.jpg	/storage/runtime/thumbs/EVT-RT-742BC921.jpg
SNP-RT-4F93D708	EVT-RT-1601262E	/storage/runtime/EVT-RT-1601262E.jpg	/storage/runtime/thumbs/EVT-RT-1601262E.jpg
SNP-RT-A58F1E66	EVT-RT-005247E1	/storage/runtime/EVT-RT-005247E1.jpg	/storage/runtime/thumbs/EVT-RT-005247E1.jpg
SNP-RT-E8BE3695	EVT-RT-46EDDC05	/storage/runtime/EVT-RT-46EDDC05.jpg	/storage/runtime/thumbs/EVT-RT-46EDDC05.jpg
SNP-RT-D29926B9	EVT-RT-B49D9895	/storage/runtime/EVT-RT-B49D9895.jpg	/storage/runtime/thumbs/EVT-RT-B49D9895.jpg
SNP-RT-5C8F5F59	EVT-RT-40E7E3F0	/storage/runtime/EVT-RT-40E7E3F0.jpg	/storage/runtime/thumbs/EVT-RT-40E7E3F0.jpg
SNP-RT-12A0F44C	EVT-RT-F925007A	/storage/runtime/EVT-RT-F925007A.jpg	/storage/runtime/thumbs/EVT-RT-F925007A.jpg
SNP-RT-9A45DCEF	EVT-RT-983B7A3E	/storage/runtime/EVT-RT-983B7A3E.jpg	/storage/runtime/thumbs/EVT-RT-983B7A3E.jpg
SNP-RT-03D631D2	EVT-RT-0E648378	/storage/runtime/EVT-RT-0E648378.jpg	/storage/runtime/thumbs/EVT-RT-0E648378.jpg
SNP-RT-7AFD36E7	EVT-RT-97ADA9F5	/storage/runtime/EVT-RT-97ADA9F5.jpg	/storage/runtime/thumbs/EVT-RT-97ADA9F5.jpg
SNP-RT-BE9722E5	EVT-RT-11BCF260	/storage/runtime/EVT-RT-11BCF260.jpg	/storage/runtime/thumbs/EVT-RT-11BCF260.jpg
SNP-RT-EF09EE99	EVT-RT-28A01B9D	/storage/runtime/EVT-RT-28A01B9D.jpg	/storage/runtime/thumbs/EVT-RT-28A01B9D.jpg
SNP-RT-B7C66EC8	EVT-RT-46EBB3F8	/storage/runtime/EVT-RT-46EBB3F8.jpg	/storage/runtime/thumbs/EVT-RT-46EBB3F8.jpg
SNP-RT-D9140C50	EVT-RT-0329AF4A	/storage/runtime/EVT-RT-0329AF4A.jpg	/storage/runtime/thumbs/EVT-RT-0329AF4A.jpg
SNP-RT-6A3D4AA5	EVT-RT-B1BF2656	/storage/runtime/EVT-RT-B1BF2656.jpg	/storage/runtime/thumbs/EVT-RT-B1BF2656.jpg
SNP-RT-6F4AAD48	EVT-RT-5A0D2CAB	/storage/runtime/EVT-RT-5A0D2CAB.jpg	/storage/runtime/thumbs/EVT-RT-5A0D2CAB.jpg
SNP-RT-B55B0A6F	EVT-RT-1C75A8AC	/storage/runtime/EVT-RT-1C75A8AC.jpg	/storage/runtime/thumbs/EVT-RT-1C75A8AC.jpg
SNP-RT-F2D9AE1A	EVT-RT-AE169985	/storage/runtime/EVT-RT-AE169985.jpg	/storage/runtime/thumbs/EVT-RT-AE169985.jpg
SNP-RT-96C47431	EVT-RT-445037A6	/storage/runtime/EVT-RT-445037A6.jpg	/storage/runtime/thumbs/EVT-RT-445037A6.jpg
SNP-RT-BAF4BB63	EVT-RT-1F2382FF	/storage/runtime/EVT-RT-1F2382FF.jpg	/storage/runtime/thumbs/EVT-RT-1F2382FF.jpg
SNP-RT-552FF62D	EVT-RT-A9415D69	/storage/runtime/EVT-RT-A9415D69.jpg	/storage/runtime/thumbs/EVT-RT-A9415D69.jpg
SNP-RT-BDE0508E	EVT-RT-0AC67C31	/storage/runtime/EVT-RT-0AC67C31.jpg	/storage/runtime/thumbs/EVT-RT-0AC67C31.jpg
SNP-RT-471195EF	EVT-RT-3D7175A3	/storage/runtime/EVT-RT-3D7175A3.jpg	/storage/runtime/thumbs/EVT-RT-3D7175A3.jpg
SNP-RT-47A4B21A	EVT-RT-DD971EF9	/storage/runtime/EVT-RT-DD971EF9.jpg	/storage/runtime/thumbs/EVT-RT-DD971EF9.jpg
SNP-RT-65F7FC3B	EVT-RT-79C9E74E	/storage/runtime/EVT-RT-79C9E74E.jpg	/storage/runtime/thumbs/EVT-RT-79C9E74E.jpg
SNP-RT-8B00993E	EVT-RT-6CBA8F56	/storage/runtime/EVT-RT-6CBA8F56.jpg	/storage/runtime/thumbs/EVT-RT-6CBA8F56.jpg
SNP-RT-4F8A5560	EVT-RT-ABD6E01F	/storage/runtime/EVT-RT-ABD6E01F.jpg	/storage/runtime/thumbs/EVT-RT-ABD6E01F.jpg
SNP-RT-9BFF1B77	EVT-RT-E3AECE57	/storage/runtime/EVT-RT-E3AECE57.jpg	/storage/runtime/thumbs/EVT-RT-E3AECE57.jpg
SNP-RT-507C8CBC	EVT-RT-E429A27B	/storage/runtime/EVT-RT-E429A27B.jpg	/storage/runtime/thumbs/EVT-RT-E429A27B.jpg
SNP-RT-7418ABA3	EVT-RT-402E8448	/storage/runtime/EVT-RT-402E8448.jpg	/storage/runtime/thumbs/EVT-RT-402E8448.jpg
SNP-RT-E3FBBF65	EVT-RT-1C4417FC	/storage/runtime/EVT-RT-1C4417FC.jpg	/storage/runtime/thumbs/EVT-RT-1C4417FC.jpg
SNP-RT-28AF1EC1	EVT-RT-5AD44F56	/storage/runtime/EVT-RT-5AD44F56.jpg	/storage/runtime/thumbs/EVT-RT-5AD44F56.jpg
SNP-RT-CC5C459A	EVT-RT-A85D7334	/storage/runtime/EVT-RT-A85D7334.jpg	/storage/runtime/thumbs/EVT-RT-A85D7334.jpg
SNP-RT-21567AED	EVT-RT-EEECA9BB	/storage/runtime/EVT-RT-EEECA9BB.jpg	/storage/runtime/thumbs/EVT-RT-EEECA9BB.jpg
SNP-RT-28C317A3	EVT-RT-21B241FC	/storage/runtime/EVT-RT-21B241FC.jpg	/storage/runtime/thumbs/EVT-RT-21B241FC.jpg
SNP-RT-15263731	EVT-RT-7D0161F8	/storage/runtime/EVT-RT-7D0161F8.jpg	/storage/runtime/thumbs/EVT-RT-7D0161F8.jpg
SNP-RT-064E86A9	EVT-RT-E15945A2	/storage/runtime/EVT-RT-E15945A2.jpg	/storage/runtime/thumbs/EVT-RT-E15945A2.jpg
SNP-RT-D6074555	EVT-RT-F80A0D7A	/storage/runtime/EVT-RT-F80A0D7A.jpg	/storage/runtime/thumbs/EVT-RT-F80A0D7A.jpg
SNP-RT-86A0BE27	EVT-RT-C4E974AE	/storage/runtime/EVT-RT-C4E974AE.jpg	/storage/runtime/thumbs/EVT-RT-C4E974AE.jpg
SNP-RT-919FEC7B	EVT-RT-1164035B	/storage/runtime/EVT-RT-1164035B.jpg	/storage/runtime/thumbs/EVT-RT-1164035B.jpg
SNP-RT-3630F009	EVT-RT-772E7897	/storage/runtime/EVT-RT-772E7897.jpg	/storage/runtime/thumbs/EVT-RT-772E7897.jpg
SNP-RT-C5E34664	EVT-RT-0D4E4060	/storage/runtime/EVT-RT-0D4E4060.jpg	/storage/runtime/thumbs/EVT-RT-0D4E4060.jpg
SNP-RT-8B7B7161	EVT-RT-81925D12	/storage/runtime/EVT-RT-81925D12.jpg	/storage/runtime/thumbs/EVT-RT-81925D12.jpg
SNP-RT-3698940B	EVT-RT-003CF0A2	/storage/runtime/EVT-RT-003CF0A2.jpg	/storage/runtime/thumbs/EVT-RT-003CF0A2.jpg
SNP-RT-6BB862B5	EVT-RT-613C495B	/storage/runtime/EVT-RT-613C495B.jpg	/storage/runtime/thumbs/EVT-RT-613C495B.jpg
SNP-RT-0FDA611B	EVT-RT-73C67934	/storage/runtime/EVT-RT-73C67934.jpg	/storage/runtime/thumbs/EVT-RT-73C67934.jpg
SNP-RT-E4925B7D	EVT-RT-C99CEA05	/storage/runtime/EVT-RT-C99CEA05.jpg	/storage/runtime/thumbs/EVT-RT-C99CEA05.jpg
SNP-RT-0EEFABFB	EVT-RT-E81AE02E	/storage/runtime/EVT-RT-E81AE02E.jpg	/storage/runtime/thumbs/EVT-RT-E81AE02E.jpg
SNP-RT-82A0DD6A	EVT-RT-D7AA35A8	/storage/runtime/EVT-RT-D7AA35A8.jpg	/storage/runtime/thumbs/EVT-RT-D7AA35A8.jpg
SNP-RT-51C7ABF9	EVT-RT-1E90893A	/storage/runtime/EVT-RT-1E90893A.jpg	/storage/runtime/thumbs/EVT-RT-1E90893A.jpg
SNP-RT-B1B69FDB	EVT-RT-89A6EB4E	/storage/runtime/EVT-RT-89A6EB4E.jpg	/storage/runtime/thumbs/EVT-RT-89A6EB4E.jpg
SNP-RT-83F4E235	EVT-RT-B6322AD7	/storage/runtime/EVT-RT-B6322AD7.jpg	/storage/runtime/thumbs/EVT-RT-B6322AD7.jpg
SNP-RT-A3EA61AD	EVT-RT-D26A1E81	/storage/runtime/EVT-RT-D26A1E81.jpg	/storage/runtime/thumbs/EVT-RT-D26A1E81.jpg
SNP-RT-0556E3D8	EVT-RT-D689D0D3	/storage/runtime/EVT-RT-D689D0D3.jpg	/storage/runtime/thumbs/EVT-RT-D689D0D3.jpg
SNP-RT-2CC7057A	EVT-RT-4317FDEB	/storage/runtime/EVT-RT-4317FDEB.jpg	/storage/runtime/thumbs/EVT-RT-4317FDEB.jpg
SNP-RT-5AA8AC1F	EVT-RT-413A8029	/storage/runtime/EVT-RT-413A8029.jpg	/storage/runtime/thumbs/EVT-RT-413A8029.jpg
SNP-RT-C6D400A4	EVT-RT-2F01612B	/storage/runtime/EVT-RT-2F01612B.jpg	/storage/runtime/thumbs/EVT-RT-2F01612B.jpg
SNP-RT-CE6250BF	EVT-RT-02D41BB8	/storage/runtime/EVT-RT-02D41BB8.jpg	/storage/runtime/thumbs/EVT-RT-02D41BB8.jpg
SNP-RT-8192C1DC	EVT-RT-B12F7CA0	/storage/runtime/EVT-RT-B12F7CA0.jpg	/storage/runtime/thumbs/EVT-RT-B12F7CA0.jpg
SNP-RT-A0421BA8	EVT-RT-138FD32B	/storage/runtime/EVT-RT-138FD32B.jpg	/storage/runtime/thumbs/EVT-RT-138FD32B.jpg
SNP-RT-E2B3EEC9	EVT-RT-ECBF4A37	/storage/runtime/EVT-RT-ECBF4A37.jpg	/storage/runtime/thumbs/EVT-RT-ECBF4A37.jpg
SNP-RT-FD4915EA	EVT-RT-76C289CD	/storage/runtime/EVT-RT-76C289CD.jpg	/storage/runtime/thumbs/EVT-RT-76C289CD.jpg
SNP-RT-889DAE64	EVT-RT-BC96516B	/storage/runtime/EVT-RT-BC96516B.jpg	/storage/runtime/thumbs/EVT-RT-BC96516B.jpg
SNP-RT-2DF62FD9	EVT-RT-F83A7242	/storage/runtime/EVT-RT-F83A7242.jpg	/storage/runtime/thumbs/EVT-RT-F83A7242.jpg
SNP-RT-5F94035C	EVT-RT-C0B71764	/storage/runtime/EVT-RT-C0B71764.jpg	/storage/runtime/thumbs/EVT-RT-C0B71764.jpg
SNP-RT-0B74C7D8	EVT-RT-F712DB9E	/storage/runtime/EVT-RT-F712DB9E.jpg	/storage/runtime/thumbs/EVT-RT-F712DB9E.jpg
SNP-RT-67E814EF	EVT-RT-1B63D861	/storage/runtime/EVT-RT-1B63D861.jpg	/storage/runtime/thumbs/EVT-RT-1B63D861.jpg
SNP-RT-0740C0F1	EVT-RT-90F85F4D	/storage/runtime/EVT-RT-90F85F4D.jpg	/storage/runtime/thumbs/EVT-RT-90F85F4D.jpg
SNP-RT-E9FDF2A7	EVT-RT-8CD99719	/storage/runtime/EVT-RT-8CD99719.jpg	/storage/runtime/thumbs/EVT-RT-8CD99719.jpg
SNP-RT-466DAC58	EVT-RT-52986ADA	/storage/runtime/EVT-RT-52986ADA.jpg	/storage/runtime/thumbs/EVT-RT-52986ADA.jpg
SNP-RT-38896A15	EVT-RT-0E388E10	/storage/runtime/EVT-RT-0E388E10.jpg	/storage/runtime/thumbs/EVT-RT-0E388E10.jpg
SNP-BIO-B15E1BBB	EVT-BIO-A5EF2334	/storage/biosecurity/EVT-BIO-A5EF2334.jpg	/storage/biosecurity/thumbs/EVT-BIO-A5EF2334.jpg
SNP-RT-5F58CA16	EVT-RT-DAE56305	/storage/runtime/EVT-RT-DAE56305.jpg	/storage/runtime/thumbs/EVT-RT-DAE56305.jpg
SNP-BIO-2AB2F3B7	EVT-BIO-DEE399AF	/storage/biosecurity/EVT-BIO-DEE399AF.jpg	/storage/biosecurity/thumbs/EVT-BIO-DEE399AF.jpg
SNP-BIO-98A3C7BF	EVT-BIO-46B5E878	/storage/biosecurity/EVT-BIO-46B5E878.jpg	/storage/biosecurity/thumbs/EVT-BIO-46B5E878.jpg
SNP-BIO-3BBF2A6C	EVT-BIO-2FDEB0F8	/storage/biosecurity/EVT-BIO-2FDEB0F8.jpg	/storage/biosecurity/thumbs/EVT-BIO-2FDEB0F8.jpg
SNP-RT-0760109A	EVT-RT-A94CA0A1	/storage/runtime/EVT-RT-A94CA0A1.jpg	/storage/runtime/thumbs/EVT-RT-A94CA0A1.jpg
SNP-BIO-95B452F8	EVT-BIO-8588D458	/storage/biosecurity/EVT-BIO-8588D458.jpg	/storage/biosecurity/thumbs/EVT-BIO-8588D458.jpg
SNP-RT-69AE7BBD	EVT-RT-BCFCCBE0	/storage/runtime/EVT-RT-BCFCCBE0.jpg	/storage/runtime/thumbs/EVT-RT-BCFCCBE0.jpg
SNP-RT-09BAD963	EVT-RT-F7C908CD	/storage/runtime/EVT-RT-F7C908CD.jpg	/storage/runtime/thumbs/EVT-RT-F7C908CD.jpg
SNP-RT-9F406360	EVT-RT-6AA9163B	/storage/runtime/EVT-RT-6AA9163B.jpg	/storage/runtime/thumbs/EVT-RT-6AA9163B.jpg
SNP-RT-6BE76F4D	EVT-RT-C5F71D7F	/storage/runtime/EVT-RT-C5F71D7F.jpg	/storage/runtime/thumbs/EVT-RT-C5F71D7F.jpg
SNP-RT-A8379BE2	EVT-RT-1FEBCC6C	/storage/runtime/EVT-RT-1FEBCC6C.jpg	/storage/runtime/thumbs/EVT-RT-1FEBCC6C.jpg
SNP-RT-4B2EEA5B	EVT-RT-D21F9CE7	/storage/runtime/EVT-RT-D21F9CE7.jpg	/storage/runtime/thumbs/EVT-RT-D21F9CE7.jpg
SNP-RT-E8ADB7BF	EVT-RT-925668E7	/storage/runtime/EVT-RT-925668E7.jpg	/storage/runtime/thumbs/EVT-RT-925668E7.jpg
SNP-RT-2DE3ADB1	EVT-RT-AC22E0AA	/storage/runtime/EVT-RT-AC22E0AA.jpg	/storage/runtime/thumbs/EVT-RT-AC22E0AA.jpg
SNP-RT-892A07FE	EVT-RT-9C1BFE70	/storage/runtime/EVT-RT-9C1BFE70.jpg	/storage/runtime/thumbs/EVT-RT-9C1BFE70.jpg
SNP-RT-6B22AA24	EVT-RT-BE6D4165	/storage/runtime/EVT-RT-BE6D4165.jpg	/storage/runtime/thumbs/EVT-RT-BE6D4165.jpg
SNP-RT-63306979	EVT-RT-20231813	/storage/runtime/EVT-RT-20231813.jpg	/storage/runtime/thumbs/EVT-RT-20231813.jpg
SNP-RT-5F90683C	EVT-RT-2937B494	/storage/runtime/EVT-RT-2937B494.jpg	/storage/runtime/thumbs/EVT-RT-2937B494.jpg
SNP-RT-6BA2F5DF	EVT-RT-322597A3	/storage/runtime/EVT-RT-322597A3.jpg	/storage/runtime/thumbs/EVT-RT-322597A3.jpg
SNP-RT-7DA12743	EVT-RT-9CDA0FE4	/storage/runtime/EVT-RT-9CDA0FE4.jpg	/storage/runtime/thumbs/EVT-RT-9CDA0FE4.jpg
SNP-RT-6F8E7D97	EVT-RT-669DF586	/storage/runtime/EVT-RT-669DF586.jpg	/storage/runtime/thumbs/EVT-RT-669DF586.jpg
SNP-RT-784C7FFD	EVT-RT-95117818	/storage/runtime/EVT-RT-95117818.jpg	/storage/runtime/thumbs/EVT-RT-95117818.jpg
SNP-RT-5FD8F7B6	EVT-RT-D756BB8B	/storage/runtime/EVT-RT-D756BB8B.jpg	/storage/runtime/thumbs/EVT-RT-D756BB8B.jpg
SNP-RT-D0B87784	EVT-RT-53C72229	/storage/runtime/EVT-RT-53C72229.jpg	/storage/runtime/thumbs/EVT-RT-53C72229.jpg
SNP-RT-CFE4B675	EVT-RT-6CEF0842	/storage/runtime/EVT-RT-6CEF0842.jpg	/storage/runtime/thumbs/EVT-RT-6CEF0842.jpg
SNP-RT-3CF6B30B	EVT-RT-F6C71382	/storage/runtime/EVT-RT-F6C71382.jpg	/storage/runtime/thumbs/EVT-RT-F6C71382.jpg
SNP-RT-6796F6B1	EVT-RT-8AC7E4CE	/storage/runtime/EVT-RT-8AC7E4CE.jpg	/storage/runtime/thumbs/EVT-RT-8AC7E4CE.jpg
SNP-RT-02B46D8F	EVT-RT-7E8A9DB8	/storage/runtime/EVT-RT-7E8A9DB8.jpg	/storage/runtime/thumbs/EVT-RT-7E8A9DB8.jpg
SNP-RT-1732F109	EVT-RT-4307A9AB	/storage/runtime/EVT-RT-4307A9AB.jpg	/storage/runtime/thumbs/EVT-RT-4307A9AB.jpg
SNP-RT-C49B7975	EVT-RT-73C1462A	/storage/runtime/EVT-RT-73C1462A.jpg	/storage/runtime/thumbs/EVT-RT-73C1462A.jpg
SNP-RT-C6CB91B2	EVT-RT-80A93610	/storage/runtime/EVT-RT-80A93610.jpg	/storage/runtime/thumbs/EVT-RT-80A93610.jpg
SNP-RT-89AF4968	EVT-RT-C010D1D7	/storage/runtime/EVT-RT-C010D1D7.jpg	/storage/runtime/thumbs/EVT-RT-C010D1D7.jpg
SNP-RT-64D0FBA1	EVT-RT-79C1C92E	/storage/runtime/EVT-RT-79C1C92E.jpg	/storage/runtime/thumbs/EVT-RT-79C1C92E.jpg
SNP-RT-F523CA84	EVT-RT-027413E3	/storage/runtime/EVT-RT-027413E3.jpg	/storage/runtime/thumbs/EVT-RT-027413E3.jpg
SNP-RT-B208CEB1	EVT-RT-60D3BE49	/storage/runtime/EVT-RT-60D3BE49.jpg	/storage/runtime/thumbs/EVT-RT-60D3BE49.jpg
SNP-RT-81B50963	EVT-RT-EDBB9C74	/storage/runtime/EVT-RT-EDBB9C74.jpg	/storage/runtime/thumbs/EVT-RT-EDBB9C74.jpg
SNP-RT-3012D5C4	EVT-RT-B14FE8A3	/storage/runtime/EVT-RT-B14FE8A3.jpg	/storage/runtime/thumbs/EVT-RT-B14FE8A3.jpg
SNP-RT-25BA14C0	EVT-RT-C056B0AD	/storage/runtime/EVT-RT-C056B0AD.jpg	/storage/runtime/thumbs/EVT-RT-C056B0AD.jpg
SNP-RT-73B4BEC2	EVT-RT-556E7387	/storage/runtime/EVT-RT-556E7387.jpg	/storage/runtime/thumbs/EVT-RT-556E7387.jpg
SNP-RT-5524ED6C	EVT-RT-262DB66A	/storage/runtime/EVT-RT-262DB66A.jpg	/storage/runtime/thumbs/EVT-RT-262DB66A.jpg
SNP-RT-45A196C5	EVT-RT-38E0A425	/storage/runtime/EVT-RT-38E0A425.jpg	/storage/runtime/thumbs/EVT-RT-38E0A425.jpg
SNP-RT-F0C17B50	EVT-RT-264ABBF5	/storage/runtime/EVT-RT-264ABBF5.jpg	/storage/runtime/thumbs/EVT-RT-264ABBF5.jpg
SNP-RT-C3DF744A	EVT-RT-94A2C0CE	/storage/runtime/EVT-RT-94A2C0CE.jpg	/storage/runtime/thumbs/EVT-RT-94A2C0CE.jpg
SNP-RT-B66C5CAC	EVT-RT-2227AE59	/storage/runtime/EVT-RT-2227AE59.jpg	/storage/runtime/thumbs/EVT-RT-2227AE59.jpg
SNP-RT-AB3DF4A2	EVT-RT-A1F7A0C6	/storage/runtime/EVT-RT-A1F7A0C6.jpg	/storage/runtime/thumbs/EVT-RT-A1F7A0C6.jpg
SNP-RT-74FF4E4D	EVT-RT-126F1D52	/storage/runtime/EVT-RT-126F1D52.jpg	/storage/runtime/thumbs/EVT-RT-126F1D52.jpg
SNP-RT-366AE0B4	EVT-RT-126B4CF0	/storage/runtime/EVT-RT-126B4CF0.jpg	/storage/runtime/thumbs/EVT-RT-126B4CF0.jpg
SNP-RT-D2DDB334	EVT-RT-91C987CE	/storage/runtime/EVT-RT-91C987CE.jpg	/storage/runtime/thumbs/EVT-RT-91C987CE.jpg
SNP-RT-22EFC9E1	EVT-RT-668DAA0B	/storage/runtime/EVT-RT-668DAA0B.jpg	/storage/runtime/thumbs/EVT-RT-668DAA0B.jpg
SNP-RT-036668F2	EVT-RT-DAA0ADEC	/storage/runtime/EVT-RT-DAA0ADEC.jpg	/storage/runtime/thumbs/EVT-RT-DAA0ADEC.jpg
SNP-RT-A8E8F6C3	EVT-RT-99626250	/storage/runtime/EVT-RT-99626250.jpg	/storage/runtime/thumbs/EVT-RT-99626250.jpg
SNP-BIO-5E6FF574	EVT-BIO-4D0342E3	/storage/biosecurity/EVT-BIO-4D0342E3.jpg	/storage/biosecurity/thumbs/EVT-BIO-4D0342E3.jpg
SNP-RT-83BF9444	EVT-RT-FF900B5A	/storage/runtime/EVT-RT-FF900B5A.jpg	/storage/runtime/thumbs/EVT-RT-FF900B5A.jpg
SNP-RT-64DBB2D8	EVT-RT-52425C1B	/storage/runtime/EVT-RT-52425C1B.jpg	/storage/runtime/thumbs/EVT-RT-52425C1B.jpg
SNP-RT-41F4145A	EVT-RT-1A5BD372	/storage/runtime/EVT-RT-1A5BD372.jpg	/storage/runtime/thumbs/EVT-RT-1A5BD372.jpg
SNP-RT-C8119B2E	EVT-RT-6740CC39	/storage/runtime/EVT-RT-6740CC39.jpg	/storage/runtime/thumbs/EVT-RT-6740CC39.jpg
SNP-RT-7FD2030A	EVT-RT-98A0A83F	/storage/runtime/EVT-RT-98A0A83F.jpg	/storage/runtime/thumbs/EVT-RT-98A0A83F.jpg
SNP-RT-CF1F584D	EVT-RT-BE49213B	/storage/runtime/EVT-RT-BE49213B.jpg	/storage/runtime/thumbs/EVT-RT-BE49213B.jpg
SNP-RT-9E609FCA	EVT-RT-669EAC64	/storage/runtime/EVT-RT-669EAC64.jpg	/storage/runtime/thumbs/EVT-RT-669EAC64.jpg
SNP-RT-F5AA451B	EVT-RT-106C239D	/storage/runtime/EVT-RT-106C239D.jpg	/storage/runtime/thumbs/EVT-RT-106C239D.jpg
SNP-RT-18C04C6A	EVT-RT-0768B32A	/storage/runtime/EVT-RT-0768B32A.jpg	/storage/runtime/thumbs/EVT-RT-0768B32A.jpg
SNP-RT-4B4C147E	EVT-RT-2ABE3773	/storage/runtime/EVT-RT-2ABE3773.jpg	/storage/runtime/thumbs/EVT-RT-2ABE3773.jpg
SNP-RT-A44F3401	EVT-RT-AE03A774	/storage/runtime/EVT-RT-AE03A774.jpg	/storage/runtime/thumbs/EVT-RT-AE03A774.jpg
SNP-RT-3869E355	EVT-RT-79A62D89	/storage/runtime/EVT-RT-79A62D89.jpg	/storage/runtime/thumbs/EVT-RT-79A62D89.jpg
SNP-RT-0F40B5B9	EVT-RT-FA337C07	/storage/runtime/EVT-RT-FA337C07.jpg	/storage/runtime/thumbs/EVT-RT-FA337C07.jpg
SNP-RT-3A52F4CA	EVT-RT-0B6CBA8E	/storage/runtime/EVT-RT-0B6CBA8E.jpg	/storage/runtime/thumbs/EVT-RT-0B6CBA8E.jpg
SNP-RT-8D0D08DF	EVT-RT-D82FB6D0	/storage/runtime/EVT-RT-D82FB6D0.jpg	/storage/runtime/thumbs/EVT-RT-D82FB6D0.jpg
SNP-RT-61EDEB67	EVT-RT-287FD0FE	/storage/runtime/EVT-RT-287FD0FE.jpg	/storage/runtime/thumbs/EVT-RT-287FD0FE.jpg
SNP-RT-7C9C2951	EVT-RT-FE5F5541	/storage/runtime/EVT-RT-FE5F5541.jpg	/storage/runtime/thumbs/EVT-RT-FE5F5541.jpg
SNP-RT-DB544B4D	EVT-RT-523A8E57	/storage/runtime/EVT-RT-523A8E57.jpg	/storage/runtime/thumbs/EVT-RT-523A8E57.jpg
SNP-RT-A0BB4A19	EVT-RT-D34DE4C4	/storage/runtime/EVT-RT-D34DE4C4.jpg	/storage/runtime/thumbs/EVT-RT-D34DE4C4.jpg
SNP-RT-AFA57271	EVT-RT-FA0468B4	/storage/runtime/EVT-RT-FA0468B4.jpg	/storage/runtime/thumbs/EVT-RT-FA0468B4.jpg
SNP-RT-993C4DA9	EVT-RT-8BCE368A	/storage/runtime/EVT-RT-8BCE368A.jpg	/storage/runtime/thumbs/EVT-RT-8BCE368A.jpg
SNP-RT-FF8C9F78	EVT-RT-8E6FEA13	/storage/runtime/EVT-RT-8E6FEA13.jpg	/storage/runtime/thumbs/EVT-RT-8E6FEA13.jpg
SNP-RT-63A5AE73	EVT-RT-D861E2EC	/storage/runtime/EVT-RT-D861E2EC.jpg	/storage/runtime/thumbs/EVT-RT-D861E2EC.jpg
SNP-RT-7309E181	EVT-RT-A6C39563	/storage/runtime/EVT-RT-A6C39563.jpg	/storage/runtime/thumbs/EVT-RT-A6C39563.jpg
SNP-RT-540DD198	EVT-RT-6E8E2AF9	/storage/runtime/EVT-RT-6E8E2AF9.jpg	/storage/runtime/thumbs/EVT-RT-6E8E2AF9.jpg
SNP-RT-BC655464	EVT-RT-77C48643	/storage/runtime/EVT-RT-77C48643.jpg	/storage/runtime/thumbs/EVT-RT-77C48643.jpg
SNP-RT-55342885	EVT-RT-504F9EF6	/storage/runtime/EVT-RT-504F9EF6.jpg	/storage/runtime/thumbs/EVT-RT-504F9EF6.jpg
SNP-RT-2D570AD3	EVT-RT-3F439E86	/storage/runtime/EVT-RT-3F439E86.jpg	/storage/runtime/thumbs/EVT-RT-3F439E86.jpg
SNP-RT-F34FAB60	EVT-RT-93C7C1D8	/storage/runtime/EVT-RT-93C7C1D8.jpg	/storage/runtime/thumbs/EVT-RT-93C7C1D8.jpg
SNP-BIO-20F154CA	EVT-BIO-03F1C1EE	/storage/biosecurity/EVT-BIO-03F1C1EE.jpg	/storage/biosecurity/thumbs/EVT-BIO-03F1C1EE.jpg
SNP-BIO-C45D3272	EVT-BIO-4D2CA332	/storage/biosecurity/EVT-BIO-4D2CA332.jpg	/storage/biosecurity/thumbs/EVT-BIO-4D2CA332.jpg
SNP-BIO-E81C07E8	EVT-BIO-3988068E	/storage/biosecurity/EVT-BIO-3988068E.jpg	/storage/biosecurity/thumbs/EVT-BIO-3988068E.jpg
SNP-RT-51F228C8	EVT-RT-50325B06	/storage/runtime/EVT-RT-50325B06.jpg	/storage/runtime/thumbs/EVT-RT-50325B06.jpg
SNP-RT-A01FB2A1	EVT-RT-97FD0E5D	/storage/runtime/EVT-RT-97FD0E5D.jpg	/storage/runtime/thumbs/EVT-RT-97FD0E5D.jpg
SNP-RT-3E2288E4	EVT-RT-D12BBBBE	/storage/runtime/EVT-RT-D12BBBBE.jpg	/storage/runtime/thumbs/EVT-RT-D12BBBBE.jpg
SNP-RT-BE8E88AB	EVT-RT-00D9ED23	/storage/runtime/EVT-RT-00D9ED23.jpg	/storage/runtime/thumbs/EVT-RT-00D9ED23.jpg
SNP-RT-8D9A789D	EVT-RT-3CF6F2B3	/storage/runtime/EVT-RT-3CF6F2B3.jpg	/storage/runtime/thumbs/EVT-RT-3CF6F2B3.jpg
SNP-RT-64F6A7B6	EVT-RT-3054BD93	/storage/runtime/EVT-RT-3054BD93.jpg	/storage/runtime/thumbs/EVT-RT-3054BD93.jpg
SNP-RT-D2375158	EVT-RT-68167776	/storage/runtime/EVT-RT-68167776.jpg	/storage/runtime/thumbs/EVT-RT-68167776.jpg
SNP-RT-9BF7AB0D	EVT-RT-4C9BC8A5	/storage/runtime/EVT-RT-4C9BC8A5.jpg	/storage/runtime/thumbs/EVT-RT-4C9BC8A5.jpg
SNP-RT-413EE11C	EVT-RT-6879DCE7	/storage/runtime/EVT-RT-6879DCE7.jpg	/storage/runtime/thumbs/EVT-RT-6879DCE7.jpg
SNP-RT-42DF6B2F	EVT-RT-C8D19DFE	/storage/runtime/EVT-RT-C8D19DFE.jpg	/storage/runtime/thumbs/EVT-RT-C8D19DFE.jpg
SNP-RT-1AC59D99	EVT-RT-32E254AA	/storage/runtime/EVT-RT-32E254AA.jpg	/storage/runtime/thumbs/EVT-RT-32E254AA.jpg
SNP-RT-1543DA6B	EVT-RT-75354B19	/storage/runtime/EVT-RT-75354B19.jpg	/storage/runtime/thumbs/EVT-RT-75354B19.jpg
SNP-RT-6403E3EB	EVT-RT-09453D98	/storage/runtime/EVT-RT-09453D98.jpg	/storage/runtime/thumbs/EVT-RT-09453D98.jpg
SNP-RT-1D62671E	EVT-RT-12644B29	/storage/runtime/EVT-RT-12644B29.jpg	/storage/runtime/thumbs/EVT-RT-12644B29.jpg
SNP-RT-6AB8ABD1	EVT-RT-73569EFF	/storage/runtime/EVT-RT-73569EFF.jpg	/storage/runtime/thumbs/EVT-RT-73569EFF.jpg
SNP-RT-5EB604F9	EVT-RT-B3DEC004	/storage/runtime/EVT-RT-B3DEC004.jpg	/storage/runtime/thumbs/EVT-RT-B3DEC004.jpg
SNP-RT-766AFB2E	EVT-RT-F0EB84F7	/storage/runtime/EVT-RT-F0EB84F7.jpg	/storage/runtime/thumbs/EVT-RT-F0EB84F7.jpg
SNP-RT-91CEAE8E	EVT-RT-B3F1AA01	/storage/runtime/EVT-RT-B3F1AA01.jpg	/storage/runtime/thumbs/EVT-RT-B3F1AA01.jpg
SNP-RT-9BB69C51	EVT-RT-0E553980	/storage/runtime/EVT-RT-0E553980.jpg	/storage/runtime/thumbs/EVT-RT-0E553980.jpg
SNP-RT-EC453F34	EVT-RT-9FAF5365	/storage/runtime/EVT-RT-9FAF5365.jpg	/storage/runtime/thumbs/EVT-RT-9FAF5365.jpg
SNP-RT-67C45F91	EVT-RT-4969E5D5	/storage/runtime/EVT-RT-4969E5D5.jpg	/storage/runtime/thumbs/EVT-RT-4969E5D5.jpg
SNP-RT-AA2D2782	EVT-RT-F537997C	/storage/runtime/EVT-RT-F537997C.jpg	/storage/runtime/thumbs/EVT-RT-F537997C.jpg
SNP-RT-DE086F0A	EVT-RT-7C29A01C	/storage/runtime/EVT-RT-7C29A01C.jpg	/storage/runtime/thumbs/EVT-RT-7C29A01C.jpg
SNP-RT-B7EA83A4	EVT-RT-7E719E1D	/storage/runtime/EVT-RT-7E719E1D.jpg	/storage/runtime/thumbs/EVT-RT-7E719E1D.jpg
SNP-RT-CECA373B	EVT-RT-61DDB512	/storage/runtime/EVT-RT-61DDB512.jpg	/storage/runtime/thumbs/EVT-RT-61DDB512.jpg
SNP-RT-B4031EE2	EVT-RT-A4FF6D99	/storage/runtime/EVT-RT-A4FF6D99.jpg	/storage/runtime/thumbs/EVT-RT-A4FF6D99.jpg
SNP-RT-A4CD787E	EVT-RT-2A7D988A	/storage/runtime/EVT-RT-2A7D988A.jpg	/storage/runtime/thumbs/EVT-RT-2A7D988A.jpg
SNP-RT-E4E89B8D	EVT-RT-C4416FC6	/storage/runtime/EVT-RT-C4416FC6.jpg	/storage/runtime/thumbs/EVT-RT-C4416FC6.jpg
SNP-RT-7B8B1DCC	EVT-RT-CB7B7406	/storage/runtime/EVT-RT-CB7B7406.jpg	/storage/runtime/thumbs/EVT-RT-CB7B7406.jpg
SNP-RT-2B6A2078	EVT-RT-4BD63C4F	/storage/runtime/EVT-RT-4BD63C4F.jpg	/storage/runtime/thumbs/EVT-RT-4BD63C4F.jpg
SNP-RT-10418E91	EVT-RT-62821F91	/storage/runtime/EVT-RT-62821F91.jpg	/storage/runtime/thumbs/EVT-RT-62821F91.jpg
SNP-RT-DDB7FBB0	EVT-RT-62BE30DB	/storage/runtime/EVT-RT-62BE30DB.jpg	/storage/runtime/thumbs/EVT-RT-62BE30DB.jpg
SNP-RT-6774E4D2	EVT-RT-1FB78648	/storage/runtime/EVT-RT-1FB78648.jpg	/storage/runtime/thumbs/EVT-RT-1FB78648.jpg
SNP-RT-84EC6357	EVT-RT-A43EAFF5	/storage/runtime/EVT-RT-A43EAFF5.jpg	/storage/runtime/thumbs/EVT-RT-A43EAFF5.jpg
SNP-RT-80A27F6B	EVT-RT-05916F02	/storage/runtime/EVT-RT-05916F02.jpg	/storage/runtime/thumbs/EVT-RT-05916F02.jpg
SNP-RT-9148AA64	EVT-RT-6DF963D3	/storage/runtime/EVT-RT-6DF963D3.jpg	/storage/runtime/thumbs/EVT-RT-6DF963D3.jpg
SNP-RT-4FB7AAA4	EVT-RT-34486E6B	/storage/runtime/EVT-RT-34486E6B.jpg	/storage/runtime/thumbs/EVT-RT-34486E6B.jpg
SNP-RT-C71AA4E6	EVT-RT-F42681E4	/storage/runtime/EVT-RT-F42681E4.jpg	/storage/runtime/thumbs/EVT-RT-F42681E4.jpg
SNP-RT-4F85E516	EVT-RT-24CC5520	/storage/runtime/EVT-RT-24CC5520.jpg	/storage/runtime/thumbs/EVT-RT-24CC5520.jpg
SNP-RT-5D392791	EVT-RT-C432BAC4	/storage/runtime/EVT-RT-C432BAC4.jpg	/storage/runtime/thumbs/EVT-RT-C432BAC4.jpg
SNP-RT-2A83DE7A	EVT-RT-D66C3AD8	/storage/runtime/EVT-RT-D66C3AD8.jpg	/storage/runtime/thumbs/EVT-RT-D66C3AD8.jpg
SNP-RT-D6295644	EVT-RT-EFE0BF04	/storage/runtime/EVT-RT-EFE0BF04.jpg	/storage/runtime/thumbs/EVT-RT-EFE0BF04.jpg
SNP-RT-BE65F01F	EVT-RT-8729A921	/storage/runtime/EVT-RT-8729A921.jpg	/storage/runtime/thumbs/EVT-RT-8729A921.jpg
SNP-RT-6E913647	EVT-RT-9749D0BE	/storage/runtime/EVT-RT-9749D0BE.jpg	/storage/runtime/thumbs/EVT-RT-9749D0BE.jpg
SNP-RT-DE0B128A	EVT-RT-5A24C8DB	/storage/runtime/EVT-RT-5A24C8DB.jpg	/storage/runtime/thumbs/EVT-RT-5A24C8DB.jpg
SNP-RT-7023BABC	EVT-RT-243EE828	/storage/runtime/EVT-RT-243EE828.jpg	/storage/runtime/thumbs/EVT-RT-243EE828.jpg
SNP-RT-5E9B0E93	EVT-RT-8B3863FE	/storage/runtime/EVT-RT-8B3863FE.jpg	/storage/runtime/thumbs/EVT-RT-8B3863FE.jpg
SNP-RT-40E7E49C	EVT-RT-8E482A5F	/storage/runtime/EVT-RT-8E482A5F.jpg	/storage/runtime/thumbs/EVT-RT-8E482A5F.jpg
SNP-RT-FDE691C4	EVT-RT-DE6A9A56	/storage/runtime/EVT-RT-DE6A9A56.jpg	/storage/runtime/thumbs/EVT-RT-DE6A9A56.jpg
SNP-RT-3B25D0B5	EVT-RT-76DE401E	/storage/runtime/EVT-RT-76DE401E.jpg	/storage/runtime/thumbs/EVT-RT-76DE401E.jpg
SNP-RT-B8038B9C	EVT-RT-7B821CF5	/storage/runtime/EVT-RT-7B821CF5.jpg	/storage/runtime/thumbs/EVT-RT-7B821CF5.jpg
SNP-RT-B1C19168	EVT-RT-8796FD30	/storage/runtime/EVT-RT-8796FD30.jpg	/storage/runtime/thumbs/EVT-RT-8796FD30.jpg
SNP-RT-F0E757FB	EVT-RT-7BBF6AF3	/storage/runtime/EVT-RT-7BBF6AF3.jpg	/storage/runtime/thumbs/EVT-RT-7BBF6AF3.jpg
SNP-RT-6D68CEB3	EVT-RT-C29D2DF8	/storage/runtime/EVT-RT-C29D2DF8.jpg	/storage/runtime/thumbs/EVT-RT-C29D2DF8.jpg
SNP-RT-6263B431	EVT-RT-E3D13E99	/storage/runtime/EVT-RT-E3D13E99.jpg	/storage/runtime/thumbs/EVT-RT-E3D13E99.jpg
SNP-RT-ADB18917	EVT-RT-1D88100A	/storage/runtime/EVT-RT-1D88100A.jpg	/storage/runtime/thumbs/EVT-RT-1D88100A.jpg
SNP-RT-CCC878AA	EVT-RT-A3715BA1	/storage/runtime/EVT-RT-A3715BA1.jpg	/storage/runtime/thumbs/EVT-RT-A3715BA1.jpg
SNP-RT-ABADABAD	EVT-RT-706066F1	/storage/runtime/EVT-RT-706066F1.jpg	/storage/runtime/thumbs/EVT-RT-706066F1.jpg
SNP-RT-0AEF0771	EVT-RT-D84BF75A	/storage/runtime/EVT-RT-D84BF75A.jpg	/storage/runtime/thumbs/EVT-RT-D84BF75A.jpg
SNP-RT-2E015F8F	EVT-RT-CE9BC831	/storage/runtime/EVT-RT-CE9BC831.jpg	/storage/runtime/thumbs/EVT-RT-CE9BC831.jpg
SNP-RT-05D8BE62	EVT-RT-A7AD549E	/storage/runtime/EVT-RT-A7AD549E.jpg	/storage/runtime/thumbs/EVT-RT-A7AD549E.jpg
SNP-RT-DEF7CACD	EVT-RT-A5A077FD	/storage/runtime/EVT-RT-A5A077FD.jpg	/storage/runtime/thumbs/EVT-RT-A5A077FD.jpg
SNP-BIO-B9F7353C	EVT-BIO-CBFDDB69	/storage/biosecurity/EVT-BIO-CBFDDB69.jpg	/storage/biosecurity/thumbs/EVT-BIO-CBFDDB69.jpg
SNP-ANI-8D4D040B	EVT-ANI-2E610AA6	/storage/animal-intrusion/EVT-ANI-2E610AA6.jpg	/storage/animal-intrusion/thumbs/EVT-ANI-2E610AA6.jpg
SNP-ANI-E189BF91	EVT-ANI-8E8AE4BC	/storage/animal-intrusion/EVT-ANI-8E8AE4BC.jpg	/storage/animal-intrusion/thumbs/EVT-ANI-8E8AE4BC.jpg
SNP-ANI-5B329952	EVT-ANI-BAA80749	/storage/animal-intrusion/EVT-ANI-BAA80749.jpg	/storage/animal-intrusion/thumbs/EVT-ANI-BAA80749.jpg
SNP-BIO-054670C2	EVT-BIO-E757CDC1	/storage/biosecurity/EVT-BIO-E757CDC1.jpg	/storage/biosecurity/thumbs/EVT-BIO-E757CDC1.jpg
SNP-ANI-113D1B1B	EVT-ANI-D3386576	/storage/animal-intrusion/EVT-ANI-D3386576.jpg	/storage/animal-intrusion/thumbs/EVT-ANI-D3386576.jpg
SNP-RT-9A19C47F	EVT-RT-5ED4AE33	/storage/runtime/EVT-RT-5ED4AE33.jpg	/storage/runtime/thumbs/EVT-RT-5ED4AE33.jpg
SNP-RT-2598F511	EVT-RT-AE0AEFAB	/storage/runtime/EVT-RT-AE0AEFAB.jpg	/storage/runtime/thumbs/EVT-RT-AE0AEFAB.jpg
SNP-RT-515AD23A	EVT-RT-44D50ACC	/storage/runtime/EVT-RT-44D50ACC.jpg	/storage/runtime/thumbs/EVT-RT-44D50ACC.jpg
SNP-RT-6A2BDD13	EVT-RT-A6308519	/storage/runtime/EVT-RT-A6308519.jpg	/storage/runtime/thumbs/EVT-RT-A6308519.jpg
SNP-RT-F3A7873C	EVT-RT-C07885FD	/storage/runtime/EVT-RT-C07885FD.jpg	/storage/runtime/thumbs/EVT-RT-C07885FD.jpg
SNP-RT-15046878	EVT-RT-517512F6	/storage/runtime/EVT-RT-517512F6.jpg	/storage/runtime/thumbs/EVT-RT-517512F6.jpg
SNP-RT-05E3C747	EVT-RT-68B8EF40	/storage/runtime/EVT-RT-68B8EF40.jpg	/storage/runtime/thumbs/EVT-RT-68B8EF40.jpg
SNP-RT-0BD3F43F	EVT-RT-2510D1BB	/storage/runtime/EVT-RT-2510D1BB.jpg	/storage/runtime/thumbs/EVT-RT-2510D1BB.jpg
SNP-RT-4C148DF3	EVT-RT-DCEE70A5	/storage/runtime/EVT-RT-DCEE70A5.jpg	/storage/runtime/thumbs/EVT-RT-DCEE70A5.jpg
SNP-RT-85650E0D	EVT-RT-A72B8A9E	/storage/runtime/EVT-RT-A72B8A9E.jpg	/storage/runtime/thumbs/EVT-RT-A72B8A9E.jpg
SNP-WF-D14A1ACD	EVT-WF-1315C3ED	/storage/workflow/EVT-WF-1315C3ED.jpg	/storage/workflow/thumbs/EVT-WF-1315C3ED.jpg
SNP-WF-79D8A2F2	EVT-WF-060A02E4	/storage/workflow/EVT-WF-060A02E4.jpg	/storage/workflow/thumbs/EVT-WF-060A02E4.jpg
SNP-WF-AC262F8E	EVT-WF-ABF12928	/storage/workflow/EVT-WF-ABF12928.jpg	/storage/workflow/thumbs/EVT-WF-ABF12928.jpg
SNP-WF-9C3F6211	EVT-WF-CE4F72E4	/storage/workflow/EVT-WF-CE4F72E4.jpg	/storage/workflow/thumbs/EVT-WF-CE4F72E4.jpg
SNP-WF-26CFB324	EVT-WF-901C5E5D	/storage/workflow/EVT-WF-901C5E5D.jpg	/storage/workflow/thumbs/EVT-WF-901C5E5D.jpg
SNP-WF-C03B3606	EVT-WF-A48D488C	/storage/workflow/EVT-WF-A48D488C.jpg	/storage/workflow/thumbs/EVT-WF-A48D488C.jpg
SNP-WF-9BC18D57	EVT-WF-90094FD0	/storage/workflow/EVT-WF-90094FD0.jpg	/storage/workflow/thumbs/EVT-WF-90094FD0.jpg
SNP-RT-9A15179F	EVT-RT-CC593150	/storage/runtime/EVT-RT-CC593150.jpg	/storage/runtime/thumbs/EVT-RT-CC593150.jpg
SNP-RT-AFD51829	EVT-RT-9B4225A4	/storage/runtime/EVT-RT-9B4225A4.jpg	/storage/runtime/thumbs/EVT-RT-9B4225A4.jpg
SNP-WF-5A8F2F54	EVT-WF-1F0BBB7A	/storage/workflow/EVT-WF-1F0BBB7A.jpg	/storage/workflow/thumbs/EVT-WF-1F0BBB7A.jpg
SNP-RT-240125A2	EVT-RT-5350A703	/storage/runtime/EVT-RT-5350A703.jpg	/storage/runtime/thumbs/EVT-RT-5350A703.jpg
SNP-RT-48EA74B5	EVT-RT-BB25B9E5	/storage/runtime/EVT-RT-BB25B9E5.jpg	/storage/runtime/thumbs/EVT-RT-BB25B9E5.jpg
SNP-RT-193D72E0	EVT-RT-E4B62A01	/storage/runtime/EVT-RT-E4B62A01.jpg	/storage/runtime/thumbs/EVT-RT-E4B62A01.jpg
SNP-RT-D41F84E2	EVT-RT-77610B8A	/storage/runtime/EVT-RT-77610B8A.jpg	/storage/runtime/thumbs/EVT-RT-77610B8A.jpg
SNP-RT-5EC0E120	EVT-RT-042A8A0D	/storage/runtime/EVT-RT-042A8A0D.jpg	/storage/runtime/thumbs/EVT-RT-042A8A0D.jpg
SNP-RT-BDCF167C	EVT-RT-9D5BA740	/storage/runtime/EVT-RT-9D5BA740.jpg	/storage/runtime/thumbs/EVT-RT-9D5BA740.jpg
SNP-RT-670D2B6D	EVT-RT-FAED45DF	/storage/runtime/EVT-RT-FAED45DF.jpg	/storage/runtime/thumbs/EVT-RT-FAED45DF.jpg
SNP-RT-8B978266	EVT-RT-9A978146	/storage/runtime/EVT-RT-9A978146.jpg	/storage/runtime/thumbs/EVT-RT-9A978146.jpg
SNP-RT-0E8C884D	EVT-RT-40DAA38E	/storage/runtime/EVT-RT-40DAA38E.jpg	/storage/runtime/thumbs/EVT-RT-40DAA38E.jpg
SNP-RT-DBC8CD8A	EVT-RT-55DA9BE2	/storage/runtime/EVT-RT-55DA9BE2.jpg	/storage/runtime/thumbs/EVT-RT-55DA9BE2.jpg
SNP-RT-C78C0A26	EVT-RT-A717A77F	/storage/runtime/EVT-RT-A717A77F.jpg	/storage/runtime/thumbs/EVT-RT-A717A77F.jpg
SNP-RT-B9F6412B	EVT-RT-0916AD15	/storage/runtime/EVT-RT-0916AD15.jpg	/storage/runtime/thumbs/EVT-RT-0916AD15.jpg
SNP-RT-A14EE8FF	EVT-RT-75071576	/storage/runtime/EVT-RT-75071576.jpg	/storage/runtime/thumbs/EVT-RT-75071576.jpg
SNP-RT-6C749B98	EVT-RT-94B22A2A	/storage/runtime/EVT-RT-94B22A2A.jpg	/storage/runtime/thumbs/EVT-RT-94B22A2A.jpg
SNP-RT-417F3646	EVT-RT-39B46F37	/storage/runtime/EVT-RT-39B46F37.jpg	/storage/runtime/thumbs/EVT-RT-39B46F37.jpg
SNP-RT-F10B31AB	EVT-RT-08214CFB	/storage/runtime/EVT-RT-08214CFB.jpg	/storage/runtime/thumbs/EVT-RT-08214CFB.jpg
SNP-RT-0F2E261A	EVT-RT-38636402	/storage/runtime/EVT-RT-38636402.jpg	/storage/runtime/thumbs/EVT-RT-38636402.jpg
SNP-RT-F4C08919	EVT-RT-2F54AE18	/storage/runtime/EVT-RT-2F54AE18.jpg	/storage/runtime/thumbs/EVT-RT-2F54AE18.jpg
SNP-RT-3F469AE8	EVT-RT-1FC284BC	/storage/runtime/EVT-RT-1FC284BC.jpg	/storage/runtime/thumbs/EVT-RT-1FC284BC.jpg
SNP-RT-02E43133	EVT-RT-87D7DE14	/storage/runtime/EVT-RT-87D7DE14.jpg	/storage/runtime/thumbs/EVT-RT-87D7DE14.jpg
SNP-RT-5A2C50D2	EVT-RT-E7614EB2	/storage/runtime/EVT-RT-E7614EB2.jpg	/storage/runtime/thumbs/EVT-RT-E7614EB2.jpg
SNP-RT-18B8A1C4	EVT-RT-E19C7F8C	/storage/runtime/EVT-RT-E19C7F8C.jpg	/storage/runtime/thumbs/EVT-RT-E19C7F8C.jpg
SNP-RT-BD789764	EVT-RT-8979345E	/storage/runtime/EVT-RT-8979345E.jpg	/storage/runtime/thumbs/EVT-RT-8979345E.jpg
SNP-RT-2C1DEEB6	EVT-RT-03BCC394	/storage/runtime/EVT-RT-03BCC394.jpg	/storage/runtime/thumbs/EVT-RT-03BCC394.jpg
SNP-RT-6E34ED11	EVT-RT-B83DE6C6	/storage/runtime/EVT-RT-B83DE6C6.jpg	/storage/runtime/thumbs/EVT-RT-B83DE6C6.jpg
SNP-RT-ABA0945E	EVT-RT-DCAAA0E8	/storage/runtime/EVT-RT-DCAAA0E8.jpg	/storage/runtime/thumbs/EVT-RT-DCAAA0E8.jpg
SNP-RT-B23D2A13	EVT-RT-9C41953C	/storage/runtime/EVT-RT-9C41953C.jpg	/storage/runtime/thumbs/EVT-RT-9C41953C.jpg
SNP-RT-4F9BA590	EVT-RT-F33336E4	/storage/runtime/EVT-RT-F33336E4.jpg	/storage/runtime/thumbs/EVT-RT-F33336E4.jpg
SNP-RT-562C786F	EVT-RT-302AF9C6	/storage/runtime/EVT-RT-302AF9C6.jpg	/storage/runtime/thumbs/EVT-RT-302AF9C6.jpg
SNP-RT-71E8DD15	EVT-RT-490A521E	/storage/runtime/EVT-RT-490A521E.jpg	/storage/runtime/thumbs/EVT-RT-490A521E.jpg
SNP-RT-1D967C89	EVT-RT-3888C83A	/storage/runtime/EVT-RT-3888C83A.jpg	/storage/runtime/thumbs/EVT-RT-3888C83A.jpg
SNP-RT-246CB529	EVT-RT-D0240B0E	/storage/runtime/EVT-RT-D0240B0E.jpg	/storage/runtime/thumbs/EVT-RT-D0240B0E.jpg
SNP-RT-3B0E4993	EVT-RT-AD545480	/storage/runtime/EVT-RT-AD545480.jpg	/storage/runtime/thumbs/EVT-RT-AD545480.jpg
SNP-RT-5BD65339	EVT-RT-3F574785	/storage/runtime/EVT-RT-3F574785.jpg	/storage/runtime/thumbs/EVT-RT-3F574785.jpg
SNP-RT-FFEC3A8D	EVT-RT-BCB0A674	/storage/runtime/EVT-RT-BCB0A674.jpg	/storage/runtime/thumbs/EVT-RT-BCB0A674.jpg
SNP-RT-C4CED4C3	EVT-RT-83008B4F	/storage/runtime/EVT-RT-83008B4F.jpg	/storage/runtime/thumbs/EVT-RT-83008B4F.jpg
SNP-RT-93CB87E5	EVT-RT-7B15E743	/storage/runtime/EVT-RT-7B15E743.jpg	/storage/runtime/thumbs/EVT-RT-7B15E743.jpg
SNP-RT-C55F6D20	EVT-RT-47559862	/storage/runtime/EVT-RT-47559862.jpg	/storage/runtime/thumbs/EVT-RT-47559862.jpg
SNP-RT-B919AB63	EVT-RT-DAD18EA0	/storage/runtime/EVT-RT-DAD18EA0.jpg	/storage/runtime/thumbs/EVT-RT-DAD18EA0.jpg
SNP-RT-AF4737CC	EVT-RT-9357836D	/storage/runtime/EVT-RT-9357836D.jpg	/storage/runtime/thumbs/EVT-RT-9357836D.jpg
SNP-RT-160894A0	EVT-RT-127F1B8A	/storage/runtime/EVT-RT-127F1B8A.jpg	/storage/runtime/thumbs/EVT-RT-127F1B8A.jpg
SNP-RT-65772B6F	EVT-RT-B9ABB01A	/storage/runtime/EVT-RT-B9ABB01A.jpg	/storage/runtime/thumbs/EVT-RT-B9ABB01A.jpg
SNP-RT-6C2A8C3D	EVT-RT-D96B147C	/storage/runtime/EVT-RT-D96B147C.jpg	/storage/runtime/thumbs/EVT-RT-D96B147C.jpg
SNP-RT-ABBEDE36	EVT-RT-1E205229	/storage/runtime/EVT-RT-1E205229.jpg	/storage/runtime/thumbs/EVT-RT-1E205229.jpg
SNP-RT-80C867B3	EVT-RT-4AF32614	/storage/runtime/EVT-RT-4AF32614.jpg	/storage/runtime/thumbs/EVT-RT-4AF32614.jpg
SNP-RT-1E60CCE1	EVT-RT-0E46F8A8	/storage/runtime/EVT-RT-0E46F8A8.jpg	/storage/runtime/thumbs/EVT-RT-0E46F8A8.jpg
SNP-RT-04E114DE	EVT-RT-874D74CE	/storage/runtime/EVT-RT-874D74CE.jpg	/storage/runtime/thumbs/EVT-RT-874D74CE.jpg
SNP-RT-C295C72C	EVT-RT-1E1FCD3E	/storage/runtime/EVT-RT-1E1FCD3E.jpg	/storage/runtime/thumbs/EVT-RT-1E1FCD3E.jpg
SNP-RT-E2D924F9	EVT-RT-CE79CE0A	/storage/runtime/EVT-RT-CE79CE0A.jpg	/storage/runtime/thumbs/EVT-RT-CE79CE0A.jpg
SNP-RT-AA3F1CFA	EVT-RT-C95A8A0E	/storage/runtime/EVT-RT-C95A8A0E.jpg	/storage/runtime/thumbs/EVT-RT-C95A8A0E.jpg
SNP-RT-D4AB3A26	EVT-RT-7534788E	/storage/runtime/EVT-RT-7534788E.jpg	/storage/runtime/thumbs/EVT-RT-7534788E.jpg
SNP-RT-CD24C6D4	EVT-RT-1747DCB2	/storage/runtime/EVT-RT-1747DCB2.jpg	/storage/runtime/thumbs/EVT-RT-1747DCB2.jpg
SNP-RT-B01A5DDB	EVT-RT-920B3643	/storage/runtime/EVT-RT-920B3643.jpg	/storage/runtime/thumbs/EVT-RT-920B3643.jpg
SNP-RT-F9DBEE35	EVT-RT-52277007	/storage/runtime/EVT-RT-52277007.jpg	/storage/runtime/thumbs/EVT-RT-52277007.jpg
SNP-RT-FF5F1EF4	EVT-RT-1F91C61C	/storage/runtime/EVT-RT-1F91C61C.jpg	/storage/runtime/thumbs/EVT-RT-1F91C61C.jpg
SNP-RT-8F578E54	EVT-RT-040AC757	/storage/runtime/EVT-RT-040AC757.jpg	/storage/runtime/thumbs/EVT-RT-040AC757.jpg
SNP-RT-F321E0EA	EVT-RT-DC672173	/storage/runtime/EVT-RT-DC672173.jpg	/storage/runtime/thumbs/EVT-RT-DC672173.jpg
SNP-RT-8CE7777E	EVT-RT-E3F74136	/storage/runtime/EVT-RT-E3F74136.jpg	/storage/runtime/thumbs/EVT-RT-E3F74136.jpg
SNP-RT-E8D18471	EVT-RT-EE1C72FC	/storage/runtime/EVT-RT-EE1C72FC.jpg	/storage/runtime/thumbs/EVT-RT-EE1C72FC.jpg
SNP-RT-8B1182F2	EVT-RT-465C5378	/storage/runtime/EVT-RT-465C5378.jpg	/storage/runtime/thumbs/EVT-RT-465C5378.jpg
SNP-RT-2DE616B5	EVT-RT-0DC24FD7	/storage/runtime/EVT-RT-0DC24FD7.jpg	/storage/runtime/thumbs/EVT-RT-0DC24FD7.jpg
SNP-RT-DA095CBB	EVT-RT-06BAB461	/storage/runtime/EVT-RT-06BAB461.jpg	/storage/runtime/thumbs/EVT-RT-06BAB461.jpg
SNP-RT-BF3A7C4C	EVT-RT-B011B8CD	/storage/runtime/EVT-RT-B011B8CD.jpg	/storage/runtime/thumbs/EVT-RT-B011B8CD.jpg
SNP-RT-198E0B82	EVT-RT-BB297A1E	/storage/runtime/EVT-RT-BB297A1E.jpg	/storage/runtime/thumbs/EVT-RT-BB297A1E.jpg
SNP-RT-51528A55	EVT-RT-1DB45716	/storage/runtime/EVT-RT-1DB45716.jpg	/storage/runtime/thumbs/EVT-RT-1DB45716.jpg
SNP-RT-26915CBD	EVT-RT-6DBF0A6F	/storage/runtime/EVT-RT-6DBF0A6F.jpg	/storage/runtime/thumbs/EVT-RT-6DBF0A6F.jpg
SNP-RT-715949C3	EVT-RT-4B10B881	/storage/runtime/EVT-RT-4B10B881.jpg	/storage/runtime/thumbs/EVT-RT-4B10B881.jpg
SNP-RT-9B70ED5A	EVT-RT-80FD7557	/storage/runtime/EVT-RT-80FD7557.jpg	/storage/runtime/thumbs/EVT-RT-80FD7557.jpg
SNP-RT-2B5A8E23	EVT-RT-06B42C62	/storage/runtime/EVT-RT-06B42C62.jpg	/storage/runtime/thumbs/EVT-RT-06B42C62.jpg
SNP-RT-BBC987B8	EVT-RT-1C90AA58	/storage/runtime/EVT-RT-1C90AA58.jpg	/storage/runtime/thumbs/EVT-RT-1C90AA58.jpg
SNP-RT-E276C81F	EVT-RT-952C9BAB	/storage/runtime/EVT-RT-952C9BAB.jpg	/storage/runtime/thumbs/EVT-RT-952C9BAB.jpg
SNP-RT-B641868B	EVT-RT-F90EE8A7	/storage/runtime/EVT-RT-F90EE8A7.jpg	/storage/runtime/thumbs/EVT-RT-F90EE8A7.jpg
SNP-RT-F5CC7600	EVT-RT-50800B4C	/storage/runtime/EVT-RT-50800B4C.jpg	/storage/runtime/thumbs/EVT-RT-50800B4C.jpg
SNP-RT-0318AE89	EVT-RT-F9E18578	/storage/runtime/EVT-RT-F9E18578.jpg	/storage/runtime/thumbs/EVT-RT-F9E18578.jpg
SNP-RT-248EBFAB	EVT-RT-07E9DDB7	/storage/runtime/EVT-RT-07E9DDB7.jpg	/storage/runtime/thumbs/EVT-RT-07E9DDB7.jpg
SNP-RT-F6C1B06B	EVT-RT-8A91E029	/storage/runtime/EVT-RT-8A91E029.jpg	/storage/runtime/thumbs/EVT-RT-8A91E029.jpg
SNP-WF-47912C95	EVT-WF-537A8BDE	/storage/workflow/EVT-WF-537A8BDE.jpg	/storage/workflow/thumbs/EVT-WF-537A8BDE.jpg
SNP-WF-48B65CF9	EVT-WF-96887688	/storage/workflow/EVT-WF-96887688.jpg	/storage/workflow/thumbs/EVT-WF-96887688.jpg
SNP-WF-004D4659	EVT-WF-5E79B1D8	/storage/workflow/EVT-WF-5E79B1D8.jpg	/storage/workflow/thumbs/EVT-WF-5E79B1D8.jpg
SNP-WF-48DC4564	EVT-WF-F300E318	/storage/workflow/EVT-WF-F300E318.jpg	/storage/workflow/thumbs/EVT-WF-F300E318.jpg
SNP-WF-EA58827D	EVT-WF-E7EE8297	/storage/workflow/EVT-WF-E7EE8297.jpg	/storage/workflow/thumbs/EVT-WF-E7EE8297.jpg
SNP-WF-993758FC	EVT-WF-867C066E	/storage/workflow/EVT-WF-867C066E.jpg	/storage/workflow/thumbs/EVT-WF-867C066E.jpg
SNP-RT-4B898F6F	EVT-RT-300E78E2	/storage/runtime/EVT-RT-300E78E2.jpg	/storage/runtime/thumbs/EVT-RT-300E78E2.jpg
SNP-RT-91876A2E	EVT-RT-B9365C23	/storage/runtime/EVT-RT-B9365C23.jpg	/storage/runtime/thumbs/EVT-RT-B9365C23.jpg
SNP-RT-8EC37D73	EVT-RT-51561BA6	/storage/runtime/EVT-RT-51561BA6.jpg	/storage/runtime/thumbs/EVT-RT-51561BA6.jpg
SNP-RT-07A7F427	EVT-RT-2F8E7668	/storage/runtime/EVT-RT-2F8E7668.jpg	/storage/runtime/thumbs/EVT-RT-2F8E7668.jpg
SNP-RT-0F554227	EVT-RT-2EA3206A	/storage/runtime/EVT-RT-2EA3206A.jpg	/storage/runtime/thumbs/EVT-RT-2EA3206A.jpg
SNP-RT-BC5538D3	EVT-RT-0A9227A3	/storage/runtime/EVT-RT-0A9227A3.jpg	/storage/runtime/thumbs/EVT-RT-0A9227A3.jpg
SNP-RT-78987922	EVT-RT-A8071FB6	/storage/runtime/EVT-RT-A8071FB6.jpg	/storage/runtime/thumbs/EVT-RT-A8071FB6.jpg
SNP-RT-B44D2725	EVT-RT-A7A24170	/storage/runtime/EVT-RT-A7A24170.jpg	/storage/runtime/thumbs/EVT-RT-A7A24170.jpg
SNP-RT-252C3D4D	EVT-RT-D7D28C77	/storage/runtime/EVT-RT-D7D28C77.jpg	/storage/runtime/thumbs/EVT-RT-D7D28C77.jpg
SNP-RT-CD12D571	EVT-RT-0F04704E	/storage/runtime/EVT-RT-0F04704E.jpg	/storage/runtime/thumbs/EVT-RT-0F04704E.jpg
SNP-RT-5DF42562	EVT-RT-9AA0D6C5	/storage/runtime/EVT-RT-9AA0D6C5.jpg	/storage/runtime/thumbs/EVT-RT-9AA0D6C5.jpg
SNP-RT-E94920F2	EVT-RT-F765A692	/storage/runtime/EVT-RT-F765A692.jpg	/storage/runtime/thumbs/EVT-RT-F765A692.jpg
SNP-RT-DF7E13E1	EVT-RT-24285AB9	/storage/runtime/EVT-RT-24285AB9.jpg	/storage/runtime/thumbs/EVT-RT-24285AB9.jpg
SNP-RT-479B8A2E	EVT-RT-4805F23E	/storage/runtime/EVT-RT-4805F23E.jpg	/storage/runtime/thumbs/EVT-RT-4805F23E.jpg
SNP-RT-8C0A141F	EVT-RT-E13E7CB9	/storage/runtime/EVT-RT-E13E7CB9.jpg	/storage/runtime/thumbs/EVT-RT-E13E7CB9.jpg
SNP-RT-218ABC82	EVT-RT-D77F7CC8	/storage/runtime/EVT-RT-D77F7CC8.jpg	/storage/runtime/thumbs/EVT-RT-D77F7CC8.jpg
SNP-RT-6D2981AD	EVT-RT-02801074	/storage/runtime/EVT-RT-02801074.jpg	/storage/runtime/thumbs/EVT-RT-02801074.jpg
SNP-RT-18952AC7	EVT-RT-AAE0629F	/storage/runtime/EVT-RT-AAE0629F.jpg	/storage/runtime/thumbs/EVT-RT-AAE0629F.jpg
SNP-RT-0580D3C2	EVT-RT-2E09042E	/storage/runtime/EVT-RT-2E09042E.jpg	/storage/runtime/thumbs/EVT-RT-2E09042E.jpg
SNP-RT-16F09FD7	EVT-RT-58CD44C6	/storage/runtime/EVT-RT-58CD44C6.jpg	/storage/runtime/thumbs/EVT-RT-58CD44C6.jpg
SNP-RT-35328ED6	EVT-RT-CBB3FD58	/storage/runtime/EVT-RT-CBB3FD58.jpg	/storage/runtime/thumbs/EVT-RT-CBB3FD58.jpg
SNP-RT-C9355CE7	EVT-RT-649921F1	/storage/runtime/EVT-RT-649921F1.jpg	/storage/runtime/thumbs/EVT-RT-649921F1.jpg
SNP-RT-AFD8A312	EVT-RT-20F6A442	/storage/runtime/EVT-RT-20F6A442.jpg	/storage/runtime/thumbs/EVT-RT-20F6A442.jpg
SNP-RT-4FFF0942	EVT-RT-78D7F067	/storage/runtime/EVT-RT-78D7F067.jpg	/storage/runtime/thumbs/EVT-RT-78D7F067.jpg
SNP-RT-C8FA4E04	EVT-RT-00E443C2	/storage/runtime/EVT-RT-00E443C2.jpg	/storage/runtime/thumbs/EVT-RT-00E443C2.jpg
SNP-RT-8AE51310	EVT-RT-44E2C2AE	/storage/runtime/EVT-RT-44E2C2AE.jpg	/storage/runtime/thumbs/EVT-RT-44E2C2AE.jpg
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.events (id, camera_id, alert_type, zone, severity, status, handler, confidence, occurred_at, category, farm_id, violation_code) FROM stdin;
EVT-001	CAM-001	Người không đúng trang phục	Cổng trại	warning	new	Chưa phân công	82	2026-06-17T06:00:00+07:00	improper_clothing	FARM-001	\N
EVT-RT-DE295378	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	90	2026-06-17T10:13:30.136965+00:00	pig_fever	FARM-001	\N
EVT-RT-02F7DF6A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:13:46.591503+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E3500358	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T10:39:51.621664+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-08DE7C83	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T10:40:02.624466+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-17B29287	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T10:40:21.731465+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-81276D8F	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T10:40:51.825826+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-CEC94A75	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T10:41:22.072597+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-3D1B30D7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T10:41:52.334133+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BAE6E1D7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T10:42:22.456738+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-84A7C1CC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T10:42:52.567087+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8E95A8E7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T10:43:22.668123+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9BD213BC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T10:43:52.770134+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6D08308D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:44:22.837239+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D466ABAC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:44:52.953629+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-AC0705AD	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:45:23.054568+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-915DA336	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T10:45:53.161129+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6B65B8F0	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T10:46:23.256155+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BD626578	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:46:53.362602+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BE27BDC6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:47:23.473711+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-73006EA4	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T10:47:53.575527+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A480BC66	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T10:48:23.664584+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6A2EEA15	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T10:48:53.771802+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-62048F22	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:00:26.236470+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B2331059	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:00:56.302703+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A58C4061	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:01:26.414350+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-21821EFE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:01:56.509249+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-EAFE0103	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:02:26.572128+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-3CD59E0A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:02:56.677088+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8CB0CFDE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:03:26.780180+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-035FC18A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:03:56.882373+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8B98E8F6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:04:27.000738+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A62E7420	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:04:57.107395+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-890B4B35	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:05:27.215784+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BD7B3FFD	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:05:57.314639+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-98A0A83F	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	90	2026-06-17T11:48:36.608832+00:00	pig_fever	FARM-001	\N
EVT-003	CAM-003	Heo sốt bất thường	Khu nái	danger	resolved	Trần Bảo Long	96	2026-06-15T12:22:00+07:00	pig_fever	FARM-001	\N
EVT-002	CAM-002	Người và động vật xâm nhập vùng cấm	Khu nái	danger	processing	Nguyễn Minh An	89	2026-06-16T09:11:00+07:00	restricted_zone_intrusion	FARM-001	\N
EVT-004	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	85	2026-06-14T15:33:00+07:00	pig_abnormal	FARM-001	\N
EVT-005	CAM-005	Xe chưa qua khử trùng	Khu cách ly	warning	processing	Chưa phân công	92	2026-06-13T18:44:00+07:00	vehicle_disinfection	FARM-001	\N
EVT-RT-7A471A36	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:49:23.890381+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A578B0E9	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T10:49:53.996071+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9FF2F5FA	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T10:50:24.084807+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D1863B4B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:50:54.182935+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F0842F88	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T10:51:24.299473+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-DF66D38B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T10:51:54.416531+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7C31CBAF	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:52:24.602881+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-5BCE2E00	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T10:52:54.711343+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D193DAD9	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T10:53:24.807725+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B8FA3700	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:53:54.919056+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-21536871	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:54:25.013666+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-FA3F75F4	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:54:55.132581+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-CC39D3BF	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T10:55:25.244268+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8FC08AB1	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T10:55:55.324131+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6496304B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T10:56:25.449874+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-58C22B56	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T10:56:55.550523+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-046	CAM-001	Camera mất kết nối	Cổng trại	critical	new	Chưa phân công	91	2026-06-12T22:15:00+07:00	camera_offline	FARM-001	\N
EVT-047	CAM-002	Động vật xâm nhập vùng cấm	Khu nái	danger	processing	Trần Bảo Long	98	2026-06-11T08:26:00+07:00	animal_intrusion	FARM-001	\N
EVT-048	CAM-003	Vi phạm quy trình ATSH	Khu nái	critical	resolved	Phạm Thu Hà	87	2026-06-10T11:37:00+07:00	workflow_violation	FARM-001	\N
EVT-RT-BFC14B09	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T10:05:20.428434+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-ABAB9E7D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T10:05:36.019038+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6BB404E1	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:06:39.553970+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9599DF0C	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	94	2026-06-17T10:07:09.597718+00:00	pig_fever	FARM-001	\N
EVT-RT-E338BA34	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	89	2026-06-17T10:07:39.628635+00:00	pig_abnormal	FARM-001	\N
EVT-RT-70D6A36E	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	98	2026-06-17T10:08:09.672932+00:00	camera_offline	FARM-001	\N
EVT-RT-A5AD8924	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	99	2026-06-17T10:08:39.708731+00:00	vehicle_disinfection	FARM-001	\N
EVT-RT-9277B021	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T10:09:09.743585+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9A030D8C	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	89	2026-06-17T10:09:39.788975+00:00	pig_fever	FARM-001	\N
EVT-RT-34FB34CF	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	99	2026-06-17T10:10:09.827674+00:00	pig_abnormal	FARM-001	\N
EVT-RT-C46862AA	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	90	2026-06-17T10:10:39.858404+00:00	camera_offline	FARM-001	\N
EVT-RT-927CC36B	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	89	2026-06-17T10:11:09.881509+00:00	vehicle_disinfection	FARM-001	\N
EVT-RT-876895A2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T10:11:39.906509+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-2D922793	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	99	2026-06-17T10:12:09.937592+00:00	pig_fever	FARM-001	\N
EVT-RT-C423F422	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	90	2026-06-17T10:12:39.955093+00:00	pig_abnormal	FARM-001	\N
EVT-006	CAM-006	Camera mất kết nối	Hành lang chính	critical	resolved	Nguyễn Minh An	99	2026-06-12T21:55:00+07:00	camera_offline	FARM-002	\N
EVT-RT-8C2CD6F7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T10:57:25.655026+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-34B0B646	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T10:57:55.776702+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-FAE1F3A6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T10:58:25.885974+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E5959412	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T10:58:55.950266+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-189AD3CF	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T10:59:26.060144+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-15B5B56B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T10:59:56.133700+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-043	CAM-007	Heo sốt bất thường	Khu con	danger	new	Chưa phân công	88	2026-06-15T13:42:00+07:00	pig_fever	FARM-002	\N
EVT-044	CAM-008	Heo nằm bất động kéo dài	Kho thức ăn	critical	processing	Phạm Thu Hà	95	2026-06-14T16:53:00+07:00	pig_abnormal	FARM-002	\N
EVT-045	CAM-009	Xe chưa qua khử trùng	Xử lý nước	warning	resolved	Chưa phân công	84	2026-06-13T19:04:00+07:00	vehicle_disinfection	FARM-002	\N
EVT-RT-4C51ED30	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:06:27.424493+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F76AD84A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:06:57.526089+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0528AC11	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:07:27.632038+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-AB639D38	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:07:57.711335+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-01B855E7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:08:27.811917+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D11FA1B5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:08:57.905540+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BDD8026A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:09:28.088208+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7E9F006D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:09:58.184726+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9B32B69A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:10:28.276326+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7ACE6473	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:10:58.364475+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D5061419	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:11:28.441368+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1ABFE50B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:11:58.587262+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4C60F9CC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:12:28.694105+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F7C36D50	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:12:58.790527+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-666372AF	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:13:28.891697+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F190C297	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:13:58.997879+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8B9E19CA	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:14:29.071967+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8928E2BF	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:14:59.173603+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1E3F177D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:15:29.278994+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-742BC921	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:15:59.366964+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1601262E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:16:29.456080+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-005247E1	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:16:59.538560+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-46EDDC05	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:17:29.667193+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B49D9895	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:17:59.774077+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-40E7E3F0	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:18:29.875438+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F925007A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:18:59.991660+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-983B7A3E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:19:30.092595+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0E648378	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:20:00.203561+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-97ADA9F5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:20:17.067348+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-11BCF260	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:20:30.314439+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-28A01B9D	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	96	2026-06-17T11:20:47.108960+00:00	pig_fever	FARM-001	\N
EVT-RT-46EBB3F8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:21:00.419373+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0329AF4A	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	94	2026-06-17T11:21:17.156955+00:00	pig_abnormal	FARM-001	\N
EVT-RT-B1BF2656	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:21:30.469836+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-5A0D2CAB	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	93	2026-06-17T11:21:47.189710+00:00	camera_offline	FARM-001	\N
EVT-RT-1C75A8AC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:22:00.533261+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-AE169985	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	98	2026-06-17T11:22:17.226792+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-445037A6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:22:30.607188+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1F2382FF	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:22:47.259737+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A9415D69	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:23:00.715219+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0AC67C31	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	96	2026-06-17T11:23:17.288273+00:00	pig_fever	FARM-001	\N
EVT-RT-3D7175A3	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:23:30.825099+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-DD971EF9	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	95	2026-06-17T11:23:47.319252+00:00	pig_abnormal	FARM-001	\N
EVT-RT-79C9E74E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:24:00.906675+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6CBA8F56	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	95	2026-06-17T11:24:17.345356+00:00	camera_offline	FARM-001	\N
EVT-RT-ABD6E01F	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:24:30.989615+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E3AECE57	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	90	2026-06-17T11:24:47.391625+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-E429A27B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:25:01.090323+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-402E8448	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:25:10.522775+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1C4417FC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:25:15.236371+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-5AD44F56	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:25:17.417642+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A85D7334	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:25:40.632914+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-EEECA9BB	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	91	2026-06-17T11:25:47.432577+00:00	pig_fever	FARM-001	\N
EVT-RT-21B241FC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:26:10.739306+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7D0161F8	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	96	2026-06-17T11:26:17.450581+00:00	pig_abnormal	FARM-001	\N
EVT-RT-E15945A2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:26:40.852128+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F80A0D7A	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	99	2026-06-17T11:26:47.491670+00:00	camera_offline	FARM-001	\N
EVT-RT-C4E974AE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:27:10.927540+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1164035B	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	99	2026-06-17T11:27:17.519382+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-772E7897	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:27:41.033279+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0D4E4060	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:27:47.553088+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-81925D12	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:28:11.130156+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-003CF0A2	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	98	2026-06-17T11:28:17.581073+00:00	pig_fever	FARM-001	\N
EVT-RT-613C495B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:28:35.784519+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-73C67934	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:28:54.698117+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-C99CEA05	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:28:54.749984+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E81AE02E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:28:55.185606+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D7AA35A8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:29:05.889117+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1E90893A	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	92	2026-06-17T11:29:25.231629+00:00	pig_fever	FARM-001	\N
EVT-RT-89A6EB4E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:29:36.028478+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B6322AD7	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	95	2026-06-17T11:29:55.271933+00:00	pig_abnormal	FARM-001	\N
EVT-RT-D26A1E81	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:30:06.150676+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D689D0D3	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	94	2026-06-17T11:30:25.313224+00:00	camera_offline	FARM-001	\N
EVT-RT-4317FDEB	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:30:36.258597+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-413A8029	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	88	2026-06-17T11:30:55.354140+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-2F01612B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:31:06.358675+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-02D41BB8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:31:25.393155+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B12F7CA0	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:31:36.483764+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-138FD32B	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	89	2026-06-17T11:31:55.460822+00:00	pig_fever	FARM-001	\N
EVT-RT-ECBF4A37	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:32:06.630922+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-76C289CD	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	93	2026-06-17T11:32:25.502471+00:00	pig_abnormal	FARM-001	\N
EVT-RT-BC96516B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:32:36.734469+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F83A7242	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	89	2026-06-17T11:32:55.537331+00:00	camera_offline	FARM-001	\N
EVT-RT-C0B71764	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:33:06.834079+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F712DB9E	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	94	2026-06-17T11:33:25.562169+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-1B63D861	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:33:36.943492+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-90F85F4D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:33:55.613258+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8CD99719	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:34:07.074731+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-52986ADA	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	91	2026-06-17T11:34:25.640639+00:00	pig_fever	FARM-001	\N
EVT-RT-0E388E10	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:34:37.247604+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-BIO-A5EF2334	CAM-001	Biosecurity violation: Person dirty_zone to safe_zone without disinfection_zone	safe_zone	critical	new	Chưa phân công	99	2026-06-17T18:32:30+07:00	person_dirty_to_safe_without_disinfection	FARM-001	\N
EVT-RT-DAE56305	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:34:59.281482+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-BIO-DEE399AF	CAM-001	Biosecurity violation: Dog enter production_zone	production_zone	critical	new	Chưa phân công	99	2026-06-17T18:33:10+07:00	dog_enter_production	FARM-001	\N
EVT-BIO-46B5E878	CAM-001	Biosecurity violation: Cat enter production_zone	production_zone	high	new	Chưa phân công	99	2026-06-17T18:33:20+07:00	cat_enter_production	FARM-001	\N
EVT-BIO-2FDEB0F8	CAM-001	Biosecurity violation: Bird enter feed_storage_zone	feed_storage_zone	warning	new	Chưa phân công	99	2026-06-17T18:33:30+07:00	bird_enter_feed_storage	FARM-001	\N
EVT-RT-A94CA0A1	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:35:07.359048+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-BIO-8588D458	CAM-001	Biosecurity violation: Vehicle outside_zone to production_zone without vehicle_d	production_zone	critical	new	Chưa phân công	99	2026-06-17T18:34:00+07:00	vehicle_outside_to_production_without_vehicle_disinfection	FARM-001	\N
EVT-RT-BCFCCBE0	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:35:37.475846+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F7C908CD	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:35:56.438206+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6AA9163B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:36:07.611346+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-C5F71D7F	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	93	2026-06-17T11:36:26.560759+00:00	pig_fever	FARM-001	\N
EVT-RT-1FEBCC6C	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:36:37.730538+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D21F9CE7	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	92	2026-06-17T11:36:56.613834+00:00	pig_abnormal	FARM-001	\N
EVT-RT-925668E7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:37:07.817207+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-AC22E0AA	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	98	2026-06-17T11:37:26.701261+00:00	camera_offline	FARM-001	\N
EVT-RT-9C1BFE70	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:37:37.894065+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BE6D4165	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	94	2026-06-17T11:37:56.754691+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-20231813	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:38:08.014138+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-2937B494	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:38:38.123632+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-322597A3	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:38:57.019639+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9CDA0FE4	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:39:08.244967+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-669DF586	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	89	2026-06-17T11:39:27.050801+00:00	pig_fever	FARM-001	\N
EVT-RT-95117818	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:39:38.345341+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D756BB8B	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	99	2026-06-17T11:39:57.097279+00:00	pig_abnormal	FARM-001	\N
EVT-RT-53C72229	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:40:08.439632+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6CEF0842	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	99	2026-06-17T11:40:27.136671+00:00	camera_offline	FARM-001	\N
EVT-RT-F6C71382	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:40:38.560413+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8AC7E4CE	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	97	2026-06-17T11:40:57.180904+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-7E8A9DB8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:41:08.686877+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4307A9AB	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:41:27.323101+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-73C1462A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:41:38.847647+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-80A93610	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	92	2026-06-17T11:41:57.363603+00:00	pig_fever	FARM-001	\N
EVT-RT-C010D1D7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:42:08.971285+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-79C1C92E	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	94	2026-06-17T11:42:27.419535+00:00	pig_abnormal	FARM-001	\N
EVT-RT-027413E3	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:42:39.080566+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-60D3BE49	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	92	2026-06-17T11:42:57.467265+00:00	camera_offline	FARM-001	\N
EVT-RT-EDBB9C74	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:43:09.181591+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B14FE8A3	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	98	2026-06-17T11:43:27.494955+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-C056B0AD	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:43:39.281745+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-556E7387	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:43:57.525290+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-262DB66A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:44:09.433682+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-38E0A425	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	94	2026-06-17T11:44:27.566018+00:00	pig_fever	FARM-001	\N
EVT-RT-264ABBF5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:44:39.783000+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-94A2C0CE	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	89	2026-06-17T11:44:57.607156+00:00	pig_abnormal	FARM-001	\N
EVT-RT-2227AE59	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:45:09.912962+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A1F7A0C6	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	92	2026-06-17T11:45:27.644599+00:00	camera_offline	FARM-001	\N
EVT-RT-126F1D52	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:45:40.005362+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-126B4CF0	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	94	2026-06-17T11:45:57.685226+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-91C987CE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:46:10.115330+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-668DAA0B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:46:27.729251+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-DAA0ADEC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:46:40.210345+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-99626250	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:47:10.313616+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-BIO-4D0342E3	CAM-001	Biosecurity violation: Person dirty_zone to safe_zone without disinfection_zone	safe_zone	critical	new	Chưa phân công	99	2026-06-17T18:44:30+07:00	person_dirty_to_safe_without_disinfection	FARM-001	\N
EVT-RT-FF900B5A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:47:12.881843+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-52425C1B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:47:40.445012+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1A5BD372	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:48:06.579918+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6740CC39	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:48:10.589017+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BE49213B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:48:40.833956+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-106C239D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:49:10.928649+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-2ABE3773	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:49:40.999999+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-79A62D89	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:50:11.089301+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0B6CBA8E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T11:50:41.188126+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-669EAC64	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	96	2026-06-17T11:49:06.655940+00:00	pig_abnormal	FARM-001	\N
EVT-RT-0768B32A	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	88	2026-06-17T11:49:36.705063+00:00	camera_offline	FARM-001	\N
EVT-RT-AE03A774	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	92	2026-06-17T11:50:06.745164+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-FA337C07	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:50:36.781671+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D82FB6D0	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	94	2026-06-17T11:51:06.822820+00:00	pig_fever	FARM-001	\N
EVT-RT-FE5F5541	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	96	2026-06-17T11:51:36.857339+00:00	pig_abnormal	FARM-001	\N
EVT-RT-D34DE4C4	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	95	2026-06-17T11:52:06.897626+00:00	camera_offline	FARM-001	\N
EVT-RT-8BCE368A	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	92	2026-06-17T11:52:36.930718+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-D861E2EC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:53:06.966367+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6E8E2AF9	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	88	2026-06-17T11:53:36.996466+00:00	pig_fever	FARM-001	\N
EVT-RT-504F9EF6	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	90	2026-06-17T11:54:07.022484+00:00	pig_abnormal	FARM-001	\N
EVT-RT-287FD0FE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:51:11.287163+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-523A8E57	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:51:41.395002+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-FA0468B4	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T11:52:11.486684+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8E6FEA13	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T11:52:41.583010+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A6C39563	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:53:11.653452+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-77C48643	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:53:41.720658+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-3F439E86	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:54:11.802316+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-93C7C1D8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:54:42.015780+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-BIO-03F1C1EE	CAM-001	Biosecurity violation: Person parking to gestation barn without person disinfect	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T20:00:00+07:00	person_parking_to_gestation_without_disinfection	FARM-001	\N
EVT-BIO-4D2CA332	CAM-001	Biosecurity violation: Dog enter farrowing barn	farrowing_barn	critical	new	Chưa phân công	99	2026-06-17T20:03:00+07:00	dog_enter_farrowing_barn	FARM-001	\N
EVT-BIO-3988068E	CAM-001	Biosecurity violation: Vehicle parking to pig loading without vehicle disinfecti	pig_loading_zone	critical	new	Chưa phân công	99	2026-06-17T20:04:00+07:00	vehicle_parking_to_loading_without_disinfection	FARM-001	\N
EVT-RT-50325B06	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T11:55:06.396259+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-97FD0E5D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:55:12.119628+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D12BBBBE	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	92	2026-06-17T11:55:36.437062+00:00	pig_fever	FARM-001	\N
EVT-RT-00D9ED23	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T11:55:42.213517+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-3CF6F2B3	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	96	2026-06-17T11:56:06.479159+00:00	pig_abnormal	FARM-001	\N
EVT-RT-3054BD93	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:56:12.332051+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-68167776	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	98	2026-06-17T11:56:36.523101+00:00	camera_offline	FARM-001	\N
EVT-RT-4C9BC8A5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:56:42.419223+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6879DCE7	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	98	2026-06-17T11:57:06.571616+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-C8D19DFE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T11:57:12.521637+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-32E254AA	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T11:57:36.610499+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-75354B19	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T11:57:42.637592+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-09453D98	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	95	2026-06-17T11:58:06.657234+00:00	pig_fever	FARM-001	\N
EVT-RT-12644B29	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T11:58:12.721589+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-73569EFF	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	91	2026-06-17T11:58:36.687331+00:00	pig_abnormal	FARM-001	\N
EVT-RT-B3DEC004	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T11:58:42.848825+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F0EB84F7	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	96	2026-06-17T11:59:06.712218+00:00	camera_offline	FARM-001	\N
EVT-RT-B3F1AA01	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T11:59:12.936115+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0E553980	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	97	2026-06-17T11:59:36.753369+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-9FAF5365	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T11:59:43.053271+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4969E5D5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T12:00:06.779669+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F537997C	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:00:13.173016+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7C29A01C	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:00:43.389280+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7E719E1D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:01:07.958163+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-61DDB512	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:01:13.489767+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A4FF6D99	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	93	2026-06-17T12:01:37.994276+00:00	pig_fever	FARM-001	\N
EVT-RT-2A7D988A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:01:43.579065+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-C4416FC6	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	96	2026-06-17T12:02:08.040330+00:00	pig_abnormal	FARM-001	\N
EVT-RT-CB7B7406	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:02:13.659001+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4BD63C4F	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	99	2026-06-17T12:02:38.092381+00:00	camera_offline	FARM-001	\N
EVT-RT-62821F91	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:02:43.758220+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-62BE30DB	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	89	2026-06-17T12:03:08.116767+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-1FB78648	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:03:13.847926+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A43EAFF5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:03:38.181174+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-05916F02	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T12:03:43.985204+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6DF963D3	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	93	2026-06-17T12:04:08.217835+00:00	pig_fever	FARM-001	\N
EVT-RT-34486E6B	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:04:14.101038+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F42681E4	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	94	2026-06-17T12:04:38.259872+00:00	pig_abnormal	FARM-001	\N
EVT-RT-24CC5520	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:04:44.213149+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-C432BAC4	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	88	2026-06-17T12:05:08.299454+00:00	camera_offline	FARM-001	\N
EVT-RT-D66C3AD8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:05:14.359760+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-EFE0BF04	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	88	2026-06-17T12:05:38.351296+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-8729A921	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:05:44.462193+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9749D0BE	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T12:06:14.597805+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-5A24C8DB	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:06:24.017037+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-243EE828	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T12:06:44.712854+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8B3863FE	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	95	2026-06-17T12:06:54.042488+00:00	pig_fever	FARM-001	\N
EVT-RT-8E482A5F	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:07:14.811081+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-DE6A9A56	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	90	2026-06-17T12:07:24.100045+00:00	pig_abnormal	FARM-001	\N
EVT-RT-76DE401E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:07:44.919657+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7B821CF5	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	94	2026-06-17T12:07:54.118079+00:00	camera_offline	FARM-001	\N
EVT-RT-8796FD30	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:08:15.001423+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7BBF6AF3	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	93	2026-06-17T12:08:24.152451+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-C29D2DF8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T12:08:45.094246+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E3D13E99	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:09:06.574699+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1D88100A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:09:15.205817+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A3715BA1	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	91	2026-06-17T12:09:36.622634+00:00	pig_fever	FARM-001	\N
EVT-RT-706066F1	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:09:45.342612+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D84BF75A	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	93	2026-06-17T12:10:06.663667+00:00	pig_abnormal	FARM-001	\N
EVT-RT-CE9BC831	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:10:15.425863+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A7AD549E	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	98	2026-06-17T12:10:36.715590+00:00	camera_offline	FARM-001	\N
EVT-RT-A5A077FD	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:10:45.507680+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-007	CAM-007	Động vật xâm nhập vùng cấm	Khu con	danger	new	Chưa phân công	88	2026-06-11T07:06:00+07:00	animal_intrusion	FARM-002	\N
EVT-BIO-CBFDDB69	CAM-001	Biosecurity violation: Dog enter gestation barn	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T23:02:00+07:00	dog_enter_gestation_barn	FARM-001	\N
EVT-ANI-2E610AA6	CAM-001	Animal intrusion: dog entered gestation_barn	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T23:02:00+07:00	animal_intrusion	FARM-001	\N
EVT-ANI-8E8AE4BC	CAM-001	Animal intrusion: cat entered farrowing_barn	farrowing_barn	high	new	Chưa phân công	99	2026-06-17T23:03:00+07:00	animal_intrusion	FARM-001	\N
EVT-ANI-BAA80749	CAM-001	Animal intrusion: rat entered vet_medicine_storage	vet_medicine_storage	critical	new	Chưa phân công	99	2026-06-17T23:04:00+07:00	animal_intrusion	FARM-001	\N
EVT-BIO-E757CDC1	CAM-001	Biosecurity violation: Bird enter feed storage	feed_storage	warning	new	Chưa phân công	99	2026-06-17T23:05:00+07:00	bird_enter_feed_storage	FARM-001	\N
EVT-ANI-D3386576	CAM-001	Animal intrusion: bird entered feed_storage	feed_storage	warning	new	Chưa phân công	99	2026-06-17T23:05:00+07:00	animal_intrusion	FARM-001	\N
EVT-RT-5ED4AE33	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T12:11:15.575523+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-AE0AEFAB	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T12:11:35.038338+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-44D50ACC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:11:45.660353+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A6308519	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	89	2026-06-17T12:12:05.070133+00:00	pig_fever	FARM-001	\N
EVT-RT-C07885FD	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T12:12:15.811234+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-517512F6	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	90	2026-06-17T12:12:35.103667+00:00	pig_abnormal	FARM-001	\N
EVT-RT-68B8EF40	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:12:45.925815+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-2510D1BB	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	94	2026-06-17T12:13:05.143510+00:00	camera_offline	FARM-001	\N
EVT-RT-DCEE70A5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T12:13:16.052884+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-008	CAM-008	Vi phạm quy trình ATSH	Kho thức ăn	critical	processing	Phạm Thu Hà	95	2026-06-10T10:17:00+07:00	workflow_violation	FARM-002	\N
EVT-009	CAM-009	Người không đúng trang phục	Xử lý nước	warning	resolved	Chưa phân công	84	2026-06-09T13:28:00+07:00	improper_clothing	FARM-002	\N
EVT-010	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-08T16:39:00+07:00	restricted_zone_intrusion	FARM-001	\N
EVT-011	CAM-002	Heo sốt bất thường	Khu nái	danger	processing	Trần Bảo Long	98	2026-06-17T19:50:00+07:00	pig_fever	FARM-001	\N
EVT-012	CAM-003	Heo nằm bất động kéo dài	Khu nái	critical	resolved	Phạm Thu Hà	87	2026-06-16T22:01:00+07:00	pig_abnormal	FARM-001	\N
EVT-013	CAM-004	Xe chưa qua khử trùng	Khu đực giống	warning	new	Chưa phân công	94	2026-06-15T08:12:00+07:00	vehicle_disinfection	FARM-001	\N
EVT-014	CAM-005	Camera mất kết nối	Khu cách ly	critical	processing	Nguyễn Minh An	83	2026-06-14T11:23:00+07:00	camera_offline	FARM-001	\N
EVT-015	CAM-006	Động vật xâm nhập vùng cấm	Hành lang chính	danger	resolved	Trần Bảo Long	90	2026-06-13T14:34:00+07:00	animal_intrusion	FARM-002	\N
EVT-016	CAM-007	Vi phạm quy trình ATSH	Khu con	critical	new	Chưa phân công	97	2026-06-12T17:45:00+07:00	workflow_violation	FARM-002	\N
EVT-017	CAM-008	Người không đúng trang phục	Kho thức ăn	warning	processing	Chưa phân công	86	2026-06-11T20:56:00+07:00	improper_clothing	FARM-002	\N
EVT-018	CAM-009	Người và động vật xâm nhập vùng cấm	Xử lý nước	danger	resolved	Nguyễn Minh An	93	2026-06-10T06:07:00+07:00	restricted_zone_intrusion	FARM-002	\N
EVT-019	CAM-001	Heo sốt bất thường	Cổng trại	danger	new	Chưa phân công	82	2026-06-09T09:18:00+07:00	pig_fever	FARM-001	\N
EVT-020	CAM-002	Heo nằm bất động kéo dài	Khu nái	critical	processing	Phạm Thu Hà	89	2026-06-08T12:29:00+07:00	pig_abnormal	FARM-001	\N
EVT-021	CAM-003	Xe chưa qua khử trùng	Khu nái	warning	resolved	Chưa phân công	96	2026-06-17T15:40:00+07:00	vehicle_disinfection	FARM-001	\N
EVT-022	CAM-004	Camera mất kết nối	Khu đực giống	critical	new	Chưa phân công	85	2026-06-16T18:51:00+07:00	camera_offline	FARM-001	\N
EVT-023	CAM-005	Động vật xâm nhập vùng cấm	Khu cách ly	danger	processing	Trần Bảo Long	92	2026-06-15T21:02:00+07:00	animal_intrusion	FARM-001	\N
EVT-024	CAM-006	Vi phạm quy trình ATSH	Hành lang chính	critical	resolved	Phạm Thu Hà	99	2026-06-14T07:13:00+07:00	workflow_violation	FARM-002	\N
EVT-025	CAM-007	Người không đúng trang phục	Khu con	warning	new	Chưa phân công	88	2026-06-13T10:24:00+07:00	improper_clothing	FARM-002	\N
EVT-026	CAM-008	Người và động vật xâm nhập vùng cấm	Kho thức ăn	danger	processing	Nguyễn Minh An	95	2026-06-12T13:35:00+07:00	restricted_zone_intrusion	FARM-002	\N
EVT-027	CAM-009	Heo sốt bất thường	Xử lý nước	danger	resolved	Trần Bảo Long	84	2026-06-11T16:46:00+07:00	pig_fever	FARM-002	\N
EVT-028	CAM-001	Heo nằm bất động kéo dài	Cổng trại	critical	new	Chưa phân công	91	2026-06-10T19:57:00+07:00	pig_abnormal	FARM-001	\N
EVT-029	CAM-002	Xe chưa qua khử trùng	Khu nái	warning	processing	Chưa phân công	98	2026-06-09T22:08:00+07:00	vehicle_disinfection	FARM-001	\N
EVT-030	CAM-003	Camera mất kết nối	Khu nái	critical	resolved	Nguyễn Minh An	87	2026-06-08T08:19:00+07:00	camera_offline	FARM-001	\N
EVT-031	CAM-004	Động vật xâm nhập vùng cấm	Khu đực giống	danger	new	Chưa phân công	94	2026-06-17T11:30:00+07:00	animal_intrusion	FARM-001	\N
EVT-032	CAM-005	Vi phạm quy trình ATSH	Khu cách ly	critical	processing	Phạm Thu Hà	83	2026-06-16T14:41:00+07:00	workflow_violation	FARM-001	\N
EVT-033	CAM-006	Người không đúng trang phục	Hành lang chính	warning	resolved	Chưa phân công	90	2026-06-15T17:52:00+07:00	improper_clothing	FARM-002	\N
EVT-034	CAM-007	Người và động vật xâm nhập vùng cấm	Khu con	danger	new	Chưa phân công	97	2026-06-14T20:03:00+07:00	restricted_zone_intrusion	FARM-002	\N
EVT-035	CAM-008	Heo sốt bất thường	Kho thức ăn	danger	processing	Trần Bảo Long	86	2026-06-13T06:14:00+07:00	pig_fever	FARM-002	\N
EVT-036	CAM-009	Heo nằm bất động kéo dài	Xử lý nước	critical	resolved	Phạm Thu Hà	93	2026-06-12T09:25:00+07:00	pig_abnormal	FARM-002	\N
EVT-037	CAM-001	Xe chưa qua khử trùng	Cổng trại	warning	new	Chưa phân công	82	2026-06-11T12:36:00+07:00	vehicle_disinfection	FARM-001	\N
EVT-038	CAM-002	Camera mất kết nối	Khu nái	critical	processing	Nguyễn Minh An	89	2026-06-10T15:47:00+07:00	camera_offline	FARM-001	\N
EVT-039	CAM-003	Động vật xâm nhập vùng cấm	Khu nái	danger	resolved	Trần Bảo Long	96	2026-06-09T18:58:00+07:00	animal_intrusion	FARM-001	\N
EVT-040	CAM-004	Vi phạm quy trình ATSH	Khu đực giống	critical	new	Chưa phân công	85	2026-06-08T21:09:00+07:00	workflow_violation	FARM-001	\N
EVT-041	CAM-005	Người không đúng trang phục	Khu cách ly	warning	processing	Chưa phân công	92	2026-06-17T07:20:00+07:00	improper_clothing	FARM-001	\N
EVT-042	CAM-006	Người và động vật xâm nhập vùng cấm	Hành lang chính	danger	resolved	Nguyễn Minh An	99	2026-06-16T10:31:00+07:00	restricted_zone_intrusion	FARM-002	\N
EVT-049	CAM-004	Người không đúng trang phục	Khu đực giống	warning	new	Chưa phân công	94	2026-06-09T14:48:00+07:00	improper_clothing	FARM-001	\N
EVT-050	CAM-005	Người và động vật xâm nhập vùng cấm	Khu cách ly	danger	processing	Nguyễn Minh An	83	2026-06-08T17:59:00+07:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A72B8A9E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:13:46.165730+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-WF-1315C3ED	CAM-001	Workflow violation: skipped required step	worker_housing	critical	new	Chưa phân công	99	2026-06-17T10:00:00+07:00	workflow_violation	FARM-001	\N
EVT-WF-060A02E4	CAM-001	Workflow violation: skipped Worker Housing	shower_room	critical	new	Chưa phân công	99	2026-06-17T10:01:00+07:00	workflow_violation	FARM-001	\N
EVT-WF-ABF12928	CAM-001	Workflow violation: skipped Worker Housing, Shower Room	handwash_zone	critical	new	Chưa phân công	99	2026-06-17T10:02:00+07:00	workflow_violation	FARM-001	\N
EVT-WF-CE4F72E4	CAM-001	Workflow violation: skipped Worker Housing, Shower Room, Handwash Zone	boot_disinfection_tray	critical	new	Chưa phân công	99	2026-06-17T10:03:00+07:00	workflow_violation	FARM-001	\N
EVT-WF-901C5E5D	CAM-001	Workflow violation: skipped Worker Housing, Shower Room, Handwash Zone, Boot Dis	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:04:00+07:00	workflow_violation	FARM-001	\N
EVT-WF-A48D488C	CAM-001	Workflow violation: skipped required step	worker_housing	critical	new	Chưa phân công	99	2026-06-17T11:00:00+07:00	workflow_violation	FARM-001	\N
EVT-WF-90094FD0	CAM-001	Workflow violation: skipped Worker Housing, Shower Room, Handwash Zone, Boot Dis	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T11:05:00+07:00	workflow_violation	FARM-001	\N
EVT-RT-CC593150	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:13:56.000302+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-9B4225A4	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T12:14:16.368092+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-WF-1F0BBB7A	CAM-001	Workflow violation: skipped Shower Room, Handwash Zone, Boot Disinfection Zone	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T14:01:00+07:00	workflow_violation	FARM-001	\N
EVT-RT-5350A703	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:14:44.991669+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BB25B9E5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:14:46.489365+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E4B62A01	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	92	2026-06-17T12:15:15.043907+00:00	pig_fever	FARM-001	\N
EVT-RT-77610B8A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:15:16.604658+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-042A8A0D	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	94	2026-06-17T12:15:45.087131+00:00	pig_abnormal	FARM-001	\N
EVT-RT-9D5BA740	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:15:46.770485+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-FAED45DF	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	97	2026-06-17T12:16:15.123157+00:00	camera_offline	FARM-001	\N
EVT-RT-9A978146	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:16:16.868550+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-40DAA38E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T12:16:47.013361+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-55DA9BE2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T12:16:50.715077+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A717A77F	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:17:17.251381+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0916AD15	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	99	2026-06-17T12:17:20.767391+00:00	pig_fever	FARM-001	\N
EVT-RT-75071576	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:17:47.434426+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-94B22A2A	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	98	2026-06-17T12:17:50.827464+00:00	pig_abnormal	FARM-001	\N
EVT-RT-39B46F37	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:18:17.537582+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-08214CFB	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	95	2026-06-17T12:18:20.897912+00:00	camera_offline	FARM-001	\N
EVT-RT-38636402	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T12:18:47.710667+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-2F54AE18	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	98	2026-06-17T12:18:50.945526+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-1FC284BC	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:19:14.815062+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-87D7DE14	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:19:36.757538+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E7614EB2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T12:19:45.010936+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-E19C7F8C	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	89	2026-06-17T12:20:06.855834+00:00	pig_fever	FARM-001	\N
EVT-RT-8979345E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:20:15.158944+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-03BCC394	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	90	2026-06-17T12:20:36.941205+00:00	pig_abnormal	FARM-001	\N
EVT-RT-B83DE6C6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T12:20:45.284812+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-DCAAA0E8	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	96	2026-06-17T12:21:07.032999+00:00	camera_offline	FARM-001	\N
EVT-RT-9C41953C	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:21:15.437544+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-490A521E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T12:22:07.229044+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-3888C83A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:22:15.733866+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7B15E743	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	91	2026-06-17T12:23:07.681083+00:00	pig_abnormal	FARM-001	\N
EVT-RT-DAD18EA0	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:23:16.040923+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-47559862	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	93	2026-06-17T12:24:07.821787+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-9357836D	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	93	2026-06-17T12:24:16.385644+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F33336E4	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	95	2026-06-17T12:21:37.139685+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-D0240B0E	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	94	2026-06-17T12:22:37.494726+00:00	pig_fever	FARM-001	\N
EVT-RT-AD545480	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	88	2026-06-17T12:23:37.756963+00:00	camera_offline	FARM-001	\N
EVT-RT-3F574785	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:24:37.916518+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-302AF9C6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:21:45.607506+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-BCB0A674	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:22:45.887584+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-83008B4F	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T12:23:46.219931+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-127F1B8A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:24:46.671895+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B9ABB01A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:25:12.951667+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D96B147C	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T12:25:16.828512+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1E205229	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:26:47.183583+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4AF32614	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:27:01.804762+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0E46F8A8	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:27:17.403104+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-874D74CE	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	88	2026-06-17T12:27:31.890043+00:00	pig_fever	FARM-001	\N
EVT-RT-1E1FCD3E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T12:27:47.553124+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-CE79CE0A	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	94	2026-06-17T12:28:01.975823+00:00	pig_abnormal	FARM-001	\N
EVT-RT-C95A8A0E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:28:17.688481+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-7534788E	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	89	2026-06-17T12:28:32.064782+00:00	camera_offline	FARM-001	\N
EVT-RT-1747DCB2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:28:47.845112+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-920B3643	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	96	2026-06-17T12:29:02.135045+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-52277007	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T12:29:48.139037+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1F91C61C	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T12:30:10.854192+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-040AC757	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:30:18.319308+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-DC672173	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	90	2026-06-17T12:30:40.921408+00:00	pig_fever	FARM-001	\N
EVT-RT-E3F74136	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:30:48.453409+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-EE1C72FC	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	96	2026-06-17T12:31:11.000101+00:00	pig_abnormal	FARM-001	\N
EVT-RT-465C5378	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:31:18.588290+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0DC24FD7	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	96	2026-06-17T12:31:41.093798+00:00	camera_offline	FARM-001	\N
EVT-RT-06BAB461	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:31:48.757559+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B011B8CD	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	93	2026-06-17T12:32:11.152568+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-BB297A1E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:32:18.906915+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-1DB45716	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:32:41.229852+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-6DBF0A6F	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:32:49.040932+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4B10B881	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	99	2026-06-17T12:33:11.302167+00:00	pig_fever	FARM-001	\N
EVT-RT-80FD7557	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:33:19.167306+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-06B42C62	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	88	2026-06-17T12:33:41.359564+00:00	pig_abnormal	FARM-001	\N
EVT-RT-1C90AA58	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T12:33:49.307830+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-952C9BAB	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	98	2026-06-17T12:34:11.430761+00:00	camera_offline	FARM-001	\N
EVT-RT-F90EE8A7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:34:19.467035+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-50800B4C	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	89	2026-06-17T12:34:41.519101+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-F9E18578	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:34:49.602705+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-07E9DDB7	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:35:11.576786+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-8A91E029	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	98	2026-06-17T12:35:19.780759+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-WF-537A8BDE	CAM-001	Vào chuồng nái: Không tắm sát trùng	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:02:00	workflow_violation	FARM-001	KHONG_TAM_SAT_TRUNG
EVT-WF-96887688	CAM-001	Vào chuồng nái: Không sát trùng tay	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:02:00	workflow_violation	FARM-001	KHONG_SAT_TRUNG_TAY
EVT-WF-5E79B1D8	CAM-001	Vào chuồng nái: Không sát trùng ủng	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:02:00	workflow_violation	FARM-001	KHONG_SAT_TRUNG_UNG
EVT-WF-F300E318	CAM-001	Vào chuồng nái: Không sát trùng tay	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:04:00	workflow_violation	FARM-001	KHONG_SAT_TRUNG_TAY
EVT-WF-E7EE8297	CAM-001	Vào chuồng nái: Không sát trùng ủng	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:04:00	workflow_violation	FARM-001	KHONG_SAT_TRUNG_UNG
EVT-WF-867C066E	CAM-001	Vào chuồng nái: Không sát trùng ủng	gestation_barn	critical	new	Chưa phân công	99	2026-06-17T10:04:00	workflow_violation	FARM-001	KHONG_SAT_TRUNG_UNG
EVT-RT-300E78E2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T12:36:19.994333+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-B9365C23	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	92	2026-06-17T12:36:34.306283+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-51561BA6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:36:50.140168+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-2F8E7668	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	96	2026-06-17T12:37:04.400230+00:00	pig_fever	FARM-001	\N
EVT-RT-2EA3206A	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:37:20.303016+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0A9227A3	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	95	2026-06-17T12:37:34.485152+00:00	pig_abnormal	FARM-001	\N
EVT-RT-A8071FB6	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T12:37:50.479419+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-A7A24170	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	96	2026-06-17T12:38:04.577998+00:00	camera_offline	FARM-001	\N
EVT-RT-D7D28C77	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:38:20.638298+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-0F04704E	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	90	2026-06-17T12:38:34.643925+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-9AA0D6C5	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:38:50.778386+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-F765A692	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	90	2026-06-17T12:39:04.716179+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-24285AB9	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	99	2026-06-17T12:39:20.972681+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-4805F23E	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	89	2026-06-17T12:39:34.804034+00:00	pig_fever	FARM-001	\N
EVT-RT-E13E7CB9	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	91	2026-06-17T12:39:51.155885+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-D77F7CC8	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	90	2026-06-17T12:40:04.887917+00:00	pig_abnormal	FARM-001	\N
EVT-RT-02801074	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	95	2026-06-17T12:40:21.334186+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-AAE0629F	CAM-005	Camera mất kết nối	Khu cách ly	critical	new	Chưa phân công	91	2026-06-17T12:40:34.973721+00:00	camera_offline	FARM-001	\N
EVT-RT-2E09042E	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	89	2026-06-17T12:40:51.507140+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-58CD44C6	CAM-008	Xe chưa qua khử trùng	Kho thức ăn	warning	new	Chưa phân công	91	2026-06-17T12:41:05.055834+00:00	vehicle_disinfection	FARM-002	\N
EVT-RT-CBB3FD58	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	97	2026-06-17T12:41:21.678034+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-649921F1	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	94	2026-06-17T12:41:35.146598+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-20F6A442	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	88	2026-06-17T12:41:51.869242+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-78D7F067	CAM-002	Heo sốt bất thường	Khu nái	danger	new	Chưa phân công	93	2026-06-17T12:42:05.238121+00:00	pig_fever	FARM-001	\N
EVT-RT-00E443C2	CAM-001	Người và động vật xâm nhập vùng cấm	Cổng trại	danger	new	Chưa phân công	96	2026-06-17T12:42:22.056842+00:00	restricted_zone_intrusion	FARM-001	\N
EVT-RT-44E2C2AE	CAM-004	Heo nằm bất động kéo dài	Khu đực giống	critical	new	Chưa phân công	93	2026-06-17T12:42:35.325725+00:00	pig_abnormal	FARM-001	\N
\.


--
-- Data for Name: farm_layout_templates; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.farm_layout_templates (id, name, description, version) FROM stdin;
TPL-PIG-STANDARD	Mẫu trại heo chuẩn AMS	Farm Layout Template chuẩn cho trại heo với 20 khu vực ATSH	3.5
\.


--
-- Data for Name: farm_map_objects; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.farm_map_objects (id, object_type, name, zone, x, y, status) FROM stdin;
MAP-001	gate	Cổng chính	Khu tiếp khách	56	74	danger
MAP-002	quarantine_zone	Chuồng cách ly	Chuồng cách ly	4	62	critical
MAP-003	disinfection_zone	Khu sát trùng xe	Khu sát trùng xe	20	60	warning
MAP-004	camera	Camera Cổng trại	Khu tiếp khách	56	74	online
MAP-005	camera	Camera Khu nái 01	Chuồng nái bầu	26	8	online
MAP-006	camera	Camera Khu đực giống	Chuồng đực giống	70	8	online
MAP-007	camera	Camera Khu cách ly	Chuồng cách ly	4	62	offline
MAP-008	disinfection_zone	Khu sát trùng người	Khu sát trùng người	20	48	warning
MAP-009	camera	Camera Kho cám	Kho cám	72	48	online
\.


--
-- Data for Name: farm_zones; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.farm_zones (id, name, risk_level, farm_id, template_id, template_zone_id, zone_code, zone_category, biosecurity_level, layout_x, layout_y, layout_w, layout_h, sort_order, active) FROM stdin;
ZONE-001	Cổng trại	danger	\N	\N	\N	legacy_zone	legacy	neutral	\N	\N	\N	\N	0	t
ZONE-002	Khu nái	warning	\N	\N	\N	legacy_zone	legacy	neutral	\N	\N	\N	\N	0	t
ZONE-003	Khu đực giống	danger	\N	\N	\N	legacy_zone	legacy	neutral	\N	\N	\N	\N	0	t
ZONE-004	Khu cách ly	critical	\N	\N	\N	legacy_zone	legacy	neutral	\N	\N	\N	\N	0	t
ZONE-005	Kho thức ăn	online	\N	\N	\N	legacy_zone	legacy	neutral	\N	\N	\N	\N	0	t
FZ-001	Chuồng cách ly	critical	FARM-001	TPL-PIG-STANDARD	TZ-001	quarantine_barn	isolation	restricted	4	62	18	14	1	t
FZ-002	Chuồng nái bầu	high	FARM-001	TPL-PIG-STANDARD	TZ-002	gestation_barn	production	clean	26	8	18	16	2	t
FZ-003	Chuồng nái đẻ	critical	FARM-001	TPL-PIG-STANDARD	TZ-003	farrowing_barn	production	clean	48	8	18	16	3	t
FZ-004	Chuồng đực giống	critical	FARM-001	TPL-PIG-STANDARD	TZ-004	boar_barn	production	clean	70	8	18	16	4	t
FZ-005	Chuồng cai sữa	high	FARM-001	TPL-PIG-STANDARD	TZ-005	weaning_barn	production	clean	26	28	18	16	5	t
FZ-006	Chuồng heo thịt	high	FARM-001	TPL-PIG-STANDARD	TZ-006	fattening_barn	production	clean	48	28	18	16	6	t
FZ-007	Nhà ở công nhân	warning	FARM-001	TPL-PIG-STANDARD	TZ-007	worker_housing	facility	dirty	4	38	14	12	7	t
FZ-008	Nhà tắm	low	FARM-001	TPL-PIG-STANDARD	TZ-008	shower_room	sanitation	neutral	4	24	14	10	8	t
FZ-009	Nhà ăn ca	warning	FARM-001	TPL-PIG-STANDARD	TZ-009	cafeteria	facility	dirty	4	12	14	10	9	t
FZ-010	Nhà bảo vệ	warning	FARM-001	TPL-PIG-STANDARD	TZ-010	guard_house	perimeter	dirty	4	2	14	8	10	t
FZ-011	Kho cám	critical	FARM-001	TPL-PIG-STANDARD	TZ-011	feed_storage	storage	restricted	72	48	14	12	11	t
FZ-012	Kho thuốc thú y	high	FARM-001	TPL-PIG-STANDARD	TZ-012	vet_medicine_storage	storage	restricted	72	62	14	12	12	t
FZ-013	Kho vật tư	warning	FARM-001	TPL-PIG-STANDARD	TZ-013	supply_storage	storage	neutral	72	76	14	10	13	t
FZ-014	Khu sát trùng người	high	FARM-001	TPL-PIG-STANDARD	TZ-014	person_disinfection_zone	sanitation	neutral	20	48	16	10	14	t
FZ-015	Khu sát trùng xe	high	FARM-001	TPL-PIG-STANDARD	TZ-015	vehicle_disinfection_zone	sanitation	neutral	20	60	16	10	15	t
FZ-016	Khu rửa tay	low	FARM-001	TPL-PIG-STANDARD	TZ-016	handwash_zone	sanitation	neutral	20	72	12	8	16	t
FZ-017	Khay sát trùng ủng	warning	FARM-001	TPL-PIG-STANDARD	TZ-017	boot_disinfection_tray	sanitation	neutral	38	48	12	8	17	t
FZ-018	Khu xuất nhập heo	high	FARM-001	TPL-PIG-STANDARD	TZ-018	pig_loading_zone	perimeter	dirty	38	58	16	12	18	t
FZ-019	Bãi đỗ xe	warning	FARM-001	TPL-PIG-STANDARD	TZ-019	parking_zone	perimeter	dirty	38	74	16	12	19	t
FZ-020	Khu tiếp khách	warning	FARM-001	TPL-PIG-STANDARD	TZ-020	reception_zone	perimeter	dirty	56	74	14	12	20	t
FZ-VI-001	Cổng trại	warning	FARM-001	TPL-PIG-STANDARD	\N	farm_gate	perimeter	dirty	22	10	12	10	1	t
FZ-VI-002	Nhà bảo vệ	warning	FARM-001	TPL-PIG-STANDARD	\N	guard_house	perimeter	dirty	34	10	12	10	2	t
FZ-VI-003	Nhà tắm sát trùng	warning	FARM-001	TPL-PIG-STANDARD	\N	shower_room	sanitation	neutral	46	10	12	10	3	t
FZ-VI-004	Nhà ăn ca	warning	FARM-001	TPL-PIG-STANDARD	\N	cafeteria	facility	dirty	58	10	12	10	4	t
FZ-VI-005	Nhà ở công nhân	warning	FARM-001	TPL-PIG-STANDARD	\N	worker_housing	facility	dirty	70	10	12	10	5	t
FZ-VI-006	Kho cám	critical	FARM-001	TPL-PIG-STANDARD	\N	feed_storage	storage	restricted	10	24	12	10	6	t
FZ-VI-007	Kho thuốc	critical	FARM-001	TPL-PIG-STANDARD	\N	vet_medicine_storage	storage	restricted	22	24	12	10	7	t
FZ-VI-008	Kho vật tư	warning	FARM-001	TPL-PIG-STANDARD	\N	supply_storage	storage	neutral	34	24	12	10	8	t
FZ-VI-009	Khu cách ly	critical	FARM-001	TPL-PIG-STANDARD	\N	quarantine_barn	isolation	restricted	46	24	12	10	9	t
FZ-VI-010	Khu đực giống	critical	FARM-001	TPL-PIG-STANDARD	\N	boar_barn	production	restricted	58	24	12	10	10	t
FZ-VI-011	Khu nái bầu	critical	FARM-001	TPL-PIG-STANDARD	\N	gestation_barn	production	restricted	70	24	12	10	11	t
FZ-VI-012	Khu nái đẻ	critical	FARM-001	TPL-PIG-STANDARD	\N	farrowing_barn	production	restricted	10	38	12	10	12	t
FZ-VI-013	Khu cai sữa	critical	FARM-001	TPL-PIG-STANDARD	\N	weaning_barn	production	restricted	22	38	12	10	13	t
FZ-VI-014	Khu heo thịt	critical	FARM-001	TPL-PIG-STANDARD	\N	fattening_barn	production	restricted	34	38	12	10	14	t
FZ-VI-015	Khu xuất bán	warning	FARM-001	TPL-PIG-STANDARD	\N	pig_loading_zone	perimeter	dirty	46	38	12	10	15	t
FZ-VI-016	Khu sát trùng xe	warning	FARM-001	TPL-PIG-STANDARD	\N	vehicle_disinfection_zone	sanitation	neutral	58	38	12	10	16	t
FZ-VI-017	Bãi đỗ xe	warning	FARM-001	TPL-PIG-STANDARD	\N	parking_zone	perimeter	dirty	70	38	12	10	17	t
FZ-VI-018	Đường nội bộ	low	FARM-001	TPL-PIG-STANDARD	\N	internal_road	movement	clean	10	52	12	10	18	t
\.


--
-- Data for Name: farms; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.farms (id, name, location, plan, status) FROM stdin;
FARM-001	AMS Farm Long An	Long An, Việt Nam	enterprise	active
FARM-002	AMS Farm Đồng Nai	Đồng Nai, Việt Nam	professional	active
\.


--
-- Data for Name: licenses; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.licenses (id, farm_id, plan, max_cameras, max_ai_models, start_date, end_date, status) FROM stdin;
LIC-001	FARM-001	enterprise	64	12	2026-01-01	2026-12-31	active
LIC-002	FARM-002	professional	32	8	2026-03-01	2027-02-28	active
\.


--
-- Data for Name: notification_gateways; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.notification_gateways (id, farm_id, gateway_type, endpoint, enabled, status) FROM stdin;
GW-001	FARM-001	telegram	@ams_farm_longan_alerts	t	online
GW-002	FARM-001	email	ops-longan@ams.local	t	online
GW-003	FARM-002	webhook	https://hooks.ams.local/dongnai	t	online
\.


--
-- Data for Name: notification_rules; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.notification_rules (id, name, alert_category, severity, email, telegram, zalo, enabled) FROM stdin;
NR-001	Thông báo Người không đúng trang phục	improper_clothing	warning	t	f	f	t
NR-002	Thông báo Người và động vật xâm nhập vùng cấm	restricted_zone_intrusion	danger	t	t	f	t
NR-003	Thông báo Heo sốt bất thường	pig_fever	danger	t	t	t	t
NR-004	Thông báo Heo nằm bất động kéo dài	pig_abnormal	critical	t	t	t	t
NR-005	Thông báo Xe chưa qua khử trùng	vehicle_disinfection	warning	t	f	f	t
NR-006	Thông báo Camera mất kết nối	camera_offline	critical	t	t	f	t
NR-007	Thông báo Động vật xâm nhập vùng cấm	animal_intrusion	danger	t	t	f	t
NR-008	Thông báo Vi phạm quy trình ATSH	workflow_violation	critical	t	t	f	t
\.


--
-- Data for Name: object_tracks; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.object_tracks (id, track_id, camera_id, object_type, current_zone, previous_zone, employee_id, enter_time, leave_time, last_seen, confidence) FROM stdin;
TRK-CAM-001-7001	7001	CAM-001	person	gestation_barn	parking_zone	EMP-001	2026-06-17T21:00:00+07:00	\N	2026-06-17T21:00:00+07:00	92.5
TRK-CAM-001-7002	7002	CAM-001	person	farrowing_barn	gestation_barn	EMP-001	2026-06-17T21:01:00+07:00	\N	2026-06-17T21:01:00+07:00	88
TRK-CAM-001-900	900	CAM-001	person	parking_zone	\N	\N	2026-06-17T22:00:00+07:00	\N	2026-06-17T22:00:00+07:00	0
TRK-CAM-001-901	901	CAM-001	person	gestation_barn	person_disinfection_zone	\N	2026-06-17T22:10:00+07:00	\N	2026-06-17T22:10:00+07:00	0
TRK-CAM-001-801	801	CAM-001	dog	parking_zone	\N	\N	2026-06-17T23:01:00+07:00	\N	2026-06-17T23:01:00+07:00	0
TRK-CAM-001-802	802	CAM-001	dog	gestation_barn	\N	\N	2026-06-17T23:02:00+07:00	\N	2026-06-17T23:02:00+07:00	0
TRK-CAM-001-803	803	CAM-001	cat	farrowing_barn	\N	\N	2026-06-17T23:03:00+07:00	\N	2026-06-17T23:03:00+07:00	0
TRK-CAM-001-804	804	CAM-001	rat	vet_medicine_storage	\N	\N	2026-06-17T23:04:00+07:00	\N	2026-06-17T23:04:00+07:00	0
TRK-CAM-001-805	805	CAM-001	bird	feed_storage	\N	\N	2026-06-17T23:05:00+07:00	\N	2026-06-17T23:05:00+07:00	0
TRK-CAM-001-9001	9001	CAM-001	person	gestation_barn	boot_disinfection_tray	\N	2026-06-17T10:00:00+07:00	\N	2026-06-17T10:04:00+07:00	0
TRK-CAM-001-9002	9002	CAM-001	person	gestation_barn	worker_housing	\N	2026-06-17T11:00:00+07:00	\N	2026-06-17T11:05:00+07:00	0
TRK-CAM-001-9101	9101	CAM-001	person	gestation_barn	boot_disinfection_tray	\N	2026-06-17T14:00:00+07:00	\N	2026-06-17T14:04:00+07:00	0
TRK-CAM-001-9102	9102	CAM-001	person	gestation_barn	worker_housing	\N	2026-06-17T14:00:00+07:00	\N	2026-06-17T14:01:00+07:00	0
TRK-CAM-001-1001	1001	CAM-001	person	gestation_barn	boot_disinfection_tray	\N	2026-06-17T10:01:00	\N	2026-06-17T10:05:00	0
TRK-CAM-001-1002	1002	CAM-001	person	gestation_barn	worker_housing	\N	2026-06-17T10:01:00	\N	2026-06-17T10:02:00	0
TRK-CAM-001-1003	1003	CAM-001	person	gestation_barn	boot_disinfection_tray	\N	2026-06-17T10:01:00	\N	2026-06-17T10:04:00	0
TRK-CAM-001-1004	1004	CAM-001	person	gestation_barn	handwash_zone	\N	2026-06-17T10:01:00	\N	2026-06-17T10:04:00	0
\.


--
-- Data for Name: person_tracks; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.person_tracks (id, track_id, camera_id, zone_id, enter_time, exit_time) FROM stdin;
PT-6C8D2463DC	1001	CAM-001	worker_housing	2026-06-17T10:01:00	2026-06-17T10:02:00
PT-8C34010A54	1001	CAM-001	shower_room	2026-06-17T10:02:00	2026-06-17T10:03:00
PT-3DCA0AE90A	1001	CAM-001	handwash_zone	2026-06-17T10:03:00	2026-06-17T10:04:00
PT-8ED696318F	1001	CAM-001	boot_disinfection_tray	2026-06-17T10:04:00	2026-06-17T10:05:00
PT-B9F825E9CE	1001	CAM-001	gestation_barn	2026-06-17T10:05:00	\N
PT-B4EA5E0E88	1002	CAM-001	worker_housing	2026-06-17T10:01:00	2026-06-17T10:02:00
PT-73FEA279C5	1002	CAM-001	gestation_barn	2026-06-17T10:02:00	\N
PT-44B40E48DF	1003	CAM-001	worker_housing	2026-06-17T10:01:00	2026-06-17T10:02:00
PT-D04840A340	1003	CAM-001	shower_room	2026-06-17T10:02:00	2026-06-17T10:03:00
PT-534E57670E	1003	CAM-001	boot_disinfection_tray	2026-06-17T10:03:00	2026-06-17T10:04:00
PT-CA4DCC44BB	1003	CAM-001	gestation_barn	2026-06-17T10:04:00	\N
PT-D37AAD8E6E	1004	CAM-001	worker_housing	2026-06-17T10:01:00	2026-06-17T10:02:00
PT-67E37488FA	1004	CAM-001	shower_room	2026-06-17T10:02:00	2026-06-17T10:03:00
PT-AF9B19A12C	1004	CAM-001	handwash_zone	2026-06-17T10:03:00	2026-06-17T10:04:00
PT-F3AABEF2E1	1004	CAM-001	gestation_barn	2026-06-17T10:04:00	\N
\.


--
-- Data for Name: template_zone_definitions; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.template_zone_definitions (id, template_id, zone_code, zone_name, zone_category, biosecurity_level, risk_level, color, layout_x, layout_y, layout_w, layout_h, sort_order) FROM stdin;
TZ-001	TPL-PIG-STANDARD	quarantine_barn	Chuồng cách ly	isolation	restricted	critical	#dc2626	4	62	18	14	1
TZ-002	TPL-PIG-STANDARD	gestation_barn	Chuồng nái bầu	production	clean	high	#16a34a	26	8	18	16	2
TZ-003	TPL-PIG-STANDARD	farrowing_barn	Chuồng nái đẻ	production	clean	critical	#15803d	48	8	18	16	3
TZ-004	TPL-PIG-STANDARD	boar_barn	Chuồng đực giống	production	clean	critical	#166534	70	8	18	16	4
TZ-005	TPL-PIG-STANDARD	weaning_barn	Chuồng cai sữa	production	clean	high	#22c55e	26	28	18	16	5
TZ-006	TPL-PIG-STANDARD	fattening_barn	Chuồng heo thịt	production	clean	high	#4ade80	48	28	18	16	6
TZ-007	TPL-PIG-STANDARD	worker_housing	Nhà ở công nhân	facility	dirty	warning	#f97316	4	38	14	12	7
TZ-008	TPL-PIG-STANDARD	shower_room	Nhà tắm	sanitation	neutral	low	#06b6d4	4	24	14	10	8
TZ-009	TPL-PIG-STANDARD	cafeteria	Nhà ăn ca	facility	dirty	warning	#fb923c	4	12	14	10	9
TZ-010	TPL-PIG-STANDARD	guard_house	Nhà bảo vệ	perimeter	dirty	warning	#ea580c	4	2	14	8	10
TZ-011	TPL-PIG-STANDARD	feed_storage	Kho cám	storage	restricted	critical	#b91c1c	72	48	14	12	11
TZ-012	TPL-PIG-STANDARD	vet_medicine_storage	Kho thuốc thú y	storage	restricted	high	#991b1b	72	62	14	12	12
TZ-013	TPL-PIG-STANDARD	supply_storage	Kho vật tư	storage	neutral	warning	#ca8a04	72	76	14	10	13
TZ-014	TPL-PIG-STANDARD	person_disinfection_zone	Khu sát trùng người	sanitation	neutral	high	#eab308	20	48	16	10	14
TZ-015	TPL-PIG-STANDARD	vehicle_disinfection_zone	Khu sát trùng xe	sanitation	neutral	high	#2563eb	20	60	16	10	15
TZ-016	TPL-PIG-STANDARD	handwash_zone	Khu rửa tay	sanitation	neutral	low	#0ea5e9	20	72	12	8	16
TZ-017	TPL-PIG-STANDARD	boot_disinfection_tray	Khay sát trùng ủng	sanitation	neutral	warning	#facc15	38	48	12	8	17
TZ-018	TPL-PIG-STANDARD	pig_loading_zone	Khu xuất nhập heo	perimeter	dirty	high	#ef4444	38	58	16	12	18
TZ-019	TPL-PIG-STANDARD	parking_zone	Bãi đỗ xe	perimeter	dirty	warning	#64748b	38	74	16	12	19
TZ-020	TPL-PIG-STANDARD	reception_zone	Khu tiếp khách	perimeter	dirty	warning	#78716c	56	74	14	12	20
\.


--
-- Data for Name: token_blacklist; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.token_blacklist (jti, user_id, expires_at) FROM stdin;
d76e1c530e6541479f57d398fa5f82fb	USR-ADMIN	1781693686
2f871b9285aa4ca2b9cc10d54b6d3ec0	USR-ADMIN	1781694320
\.


--
-- Data for Name: track_workflow_progress; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.track_workflow_progress (id, track_id, camera_id, workflow_id, completed_step_order, last_zone, updated_at) FROM stdin;
TWP-CAM-001-9001-WF-PERSON-ENTRY	9001	CAM-001	WF-PERSON-ENTRY	-1	gestation_barn	2026-06-17T10:00:00+07:00
TWP-CAM-001-9002-WF-PERSON-ENTRY	9002	CAM-001	WF-PERSON-ENTRY	-1	gestation_barn	2026-06-17T11:00:00+07:00
TWP-CAM-001-9101-WF-PERSON-ENTRY	9101	CAM-001	WF-PERSON-ENTRY	5	gestation_barn	2026-06-17T14:04:00+07:00
TWP-CAM-001-9102-WF-PERSON-ENTRY	9102	CAM-001	WF-PERSON-ENTRY	1	worker_housing	2026-06-17T14:00:00+07:00
TWP-CAM-001-1001-WF-BOAR-ENTRY	1001	CAM-001	WF-BOAR-ENTRY	4	boot_disinfection_tray	2026-06-17T10:04:00
TWP-CAM-001-1001-WF-FARROWING-ENTRY	1001	CAM-001	WF-FARROWING-ENTRY	4	boot_disinfection_tray	2026-06-17T10:04:00
TWP-CAM-001-1001-WF-GESTATION-ENTRY	1001	CAM-001	WF-GESTATION-ENTRY	5	gestation_barn	2026-06-17T10:05:00
TWP-CAM-001-1002-WF-BOAR-ENTRY	1002	CAM-001	WF-BOAR-ENTRY	1	worker_housing	2026-06-17T10:01:00
TWP-CAM-001-1002-WF-FARROWING-ENTRY	1002	CAM-001	WF-FARROWING-ENTRY	1	worker_housing	2026-06-17T10:01:00
TWP-CAM-001-1002-WF-GESTATION-ENTRY	1002	CAM-001	WF-GESTATION-ENTRY	1	worker_housing	2026-06-17T10:01:00
TWP-CAM-001-1003-WF-BOAR-ENTRY	1003	CAM-001	WF-BOAR-ENTRY	2	shower_room	2026-06-17T10:02:00
TWP-CAM-001-1003-WF-FARROWING-ENTRY	1003	CAM-001	WF-FARROWING-ENTRY	2	shower_room	2026-06-17T10:02:00
TWP-CAM-001-1003-WF-GESTATION-ENTRY	1003	CAM-001	WF-GESTATION-ENTRY	2	shower_room	2026-06-17T10:02:00
TWP-CAM-001-1004-WF-BOAR-ENTRY	1004	CAM-001	WF-BOAR-ENTRY	3	handwash_zone	2026-06-17T10:03:00
TWP-CAM-001-1004-WF-FARROWING-ENTRY	1004	CAM-001	WF-FARROWING-ENTRY	3	handwash_zone	2026-06-17T10:03:00
TWP-CAM-001-1004-WF-GESTATION-ENTRY	1004	CAM-001	WF-GESTATION-ENTRY	3	handwash_zone	2026-06-17T10:03:00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.users (id, email, full_name, role, hashed_password, is_active) FROM stdin;
USR-ADMIN	admin@ams.local	AMS Administrator	admin	pbkdf2_sha256$c6baa2b8943d43d48173d2a8ef6c6acc$f2088af22957f41cd67f593c0a4c1fe5f735a2842afc83a06f4c486158aa25f9	t
\.


--
-- Data for Name: visitors; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.visitors (id, visitor_name, company, vehicle_plate, visit_purpose, arrival_time, departure_time, approved_by) FROM stdin;
VIS-001	Nguyễn Thanh Tùng	Công ty CP Thức ăn Chăn nuôi	51A-12345	Kiểm tra quy trình cho ăn	2026-06-17T08:30:00+07:00	2026-06-17T11:00:00+07:00	Nguyễn Minh An
VIS-002	Trần Quốc Bảo	Sở NN&PTNT Long An	51B-67890	Thanh tra ATSH định kỳ	2026-06-17T09:00:00+07:00	\N	AMS Administrator
VIS-004	Phạm Văn Đức	Đại lý thuốc thú y VetPro	51C-11223	Giao thuốc kháng sinh	2026-06-17T13:15:00+07:00	\N	Phạm Thu Hà
VIS-003	Lê Thị Hồng	Công ty Thiết bị chăn nuôi ABC		Bảo trì hệ thống camera	\N	\N	Trần Bảo Long
\.


--
-- Data for Name: workflow_steps; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.workflow_steps (id, workflow_id, step_order, step_name, zone_code, required) FROM stdin;
WFS-GESTATION-ENTRY-01	WF-GESTATION-ENTRY	1	Nhà ở công nhân	worker_housing	t
WFS-GESTATION-ENTRY-02	WF-GESTATION-ENTRY	2	Nhà tắm	shower_room	t
WFS-GESTATION-ENTRY-03	WF-GESTATION-ENTRY	3	Sát trùng tay	handwash_zone	t
WFS-GESTATION-ENTRY-04	WF-GESTATION-ENTRY	4	Sát trùng ủng	boot_disinfection_tray	t
WFS-GESTATION-ENTRY-05	WF-GESTATION-ENTRY	5	Chuồng nái	gestation_barn	t
WFS-FARROWING-ENTRY-01	WF-FARROWING-ENTRY	1	Nhà ở công nhân	worker_housing	t
WFS-FARROWING-ENTRY-02	WF-FARROWING-ENTRY	2	Nhà tắm	shower_room	t
WFS-FARROWING-ENTRY-03	WF-FARROWING-ENTRY	3	Sát trùng tay	handwash_zone	t
WFS-FARROWING-ENTRY-04	WF-FARROWING-ENTRY	4	Sát trùng ủng	boot_disinfection_tray	t
WFS-FARROWING-ENTRY-05	WF-FARROWING-ENTRY	5	Chuồng đẻ	farrowing_barn	t
WFS-BOAR-ENTRY-01	WF-BOAR-ENTRY	1	Nhà ở công nhân	worker_housing	t
WFS-BOAR-ENTRY-02	WF-BOAR-ENTRY	2	Nhà tắm	shower_room	t
WFS-BOAR-ENTRY-03	WF-BOAR-ENTRY	3	Sát trùng tay	handwash_zone	t
WFS-BOAR-ENTRY-04	WF-BOAR-ENTRY	4	Sát trùng ủng	boot_disinfection_tray	t
WFS-BOAR-ENTRY-05	WF-BOAR-ENTRY	5	Chuồng đực giống	boar_barn	t
\.


--
-- Data for Name: workflows; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.workflows (id, name, description, object_type, enabled, created_at) FROM stdin;
WF-GESTATION-ENTRY	Vào chuồng nái	Nhà ở công nhân → Nhà tắm → Sát trùng tay → Sát trùng ủng → Chuồng nái	person	t	2026-06-17T12:35:21.591216+00:00
WF-FARROWING-ENTRY	Vào chuồng đẻ	Nhà ở công nhân → Nhà tắm → Sát trùng tay → Sát trùng ủng → Chuồng đẻ	person	t	2026-06-17T12:35:21.591216+00:00
WF-BOAR-ENTRY	Vào chuồng đực giống	Nhà ở công nhân → Nhà tắm → Sát trùng tay → Sát trùng ủng → Chuồng đực giống	person	t	2026-06-17T12:35:21.591216+00:00
\.


--
-- Data for Name: zone_polygons; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.zone_polygons (id, farm_id, camera_id, zone_name, zone_type, color, polygon_points, active, created_at, biosecurity_level) FROM stdin;
ZP-GATE-003	FARM-001	CAM-001	Khu sát trùng người	person_disinfection_zone	#eab308	[[750, 60], [1180, 60], [1180, 360], [750, 360]]	t	2026-06-17T18:17:00+07:00	yellow
ZP-GATE-001	FARM-001	CAM-001	Cổng trại	farm_gate	#f97316	[[40, 40], [360, 40], [360, 220], [40, 220]]	t	2026-06-17T18:17:00+07:00	orange
ZP-GATE-005	FARM-001	CAM-001	Khay sát trùng ủng	boot_disinfection_tray	#eab308	[[80, 280], [300, 280], [300, 460], [80, 460]]	t	2026-06-17T18:17:00+07:00	yellow
ZP-GATE-006	FARM-001	CAM-001	Chuồng nái bầu	gestation_barn	#dc2626	[[820, 380], [1120, 380], [1120, 620], [820, 620]]	t	2026-06-17T18:17:00+07:00	red
ZP-GATE-002	FARM-001	CAM-001	Bãi đỗ xe	parking_zone	#f97316	[[390, 40], [720, 40], [720, 240], [390, 240]]	t	2026-06-17T18:17:00+07:00	orange
ZP-GATE-004	FARM-001	CAM-001	Khu sát trùng xe	vehicle_disinfection_zone	#eab308	[[430, 280], [720, 280], [760, 500], [390, 500]]	t	2026-06-17T18:17:00+07:00	yellow
\.


--
-- Data for Name: zone_transitions; Type: TABLE DATA; Schema: public; Owner: ams
--

COPY public.zone_transitions (id, object_type, track_id, from_zone, to_zone, "timestamp", camera_id, cross_time) FROM stdin;
ZT-E6875B9BE163	person	1	handwash_zone	unknown	2026-06-17T11:28:54.619520+00:00	CAM-001	2026-06-17T11:28:54.619520+00:00
ZT-EDE20394A80D	person	1	unknown	vehicle_disinfection_zone	2026-06-17T11:28:54.721982+00:00	CAM-001	2026-06-17T11:28:54.721982+00:00
ZT-C4A0EF36F1B1	dog	2	vehicle_disinfection_zone	unknown	2026-06-17T11:30:06.055094+00:00	CAM-001	2026-06-17T11:30:06.055094+00:00
ZT-F05D8ED620DC	person	1	vehicle_disinfection_zone	restricted_zone	2026-06-17T11:30:36.178323+00:00	CAM-001	2026-06-17T11:30:36.178323+00:00
ZT-FAEFE0AC1EC1	dog	2	unknown	restricted_zone	2026-06-17T11:30:36.178323+00:00	CAM-001	2026-06-17T11:30:36.178323+00:00
ZT-70152E96FC3B	person	9091	dirty_zone	safe_zone	2026-06-17T18:32:30+07:00	CAM-001	2026-06-17T18:32:30+07:00
ZT-D7ED08D0208E	dog	9093	parking_zone	production_zone	2026-06-17T18:33:10+07:00	CAM-001	2026-06-17T18:33:10+07:00
ZT-EC007C1091FD	cat	9094	parking_zone	production_zone	2026-06-17T18:33:20+07:00	CAM-001	2026-06-17T18:33:20+07:00
ZT-E437F118D9FA	bird	9095	outside_zone	feed_storage_zone	2026-06-17T18:33:30+07:00	CAM-001	2026-06-17T18:33:30+07:00
ZT-CC26BF1B37C0	vehicle	9096	outside_zone	production_zone	2026-06-17T18:34:00+07:00	CAM-001	2026-06-17T18:34:00+07:00
ZT-DD4C1D9981BB	person	9911	dirty_zone	safe_zone	2026-06-17T18:44:30+07:00	CAM-001	2026-06-17T18:44:30+07:00
ZT-SEED-001	person	501	parking_zone	gestation_barn	2026-06-17T18:20:00+07:00	CAM-001	2026-06-17T18:20:00+07:00
ZT-SEED-002	vehicle	502	parking_zone	pig_loading_zone	2026-06-17T18:21:00+07:00	CAM-001	2026-06-17T18:21:00+07:00
ZT-SEED-003	dog	503	reception_zone	farrowing_barn	2026-06-17T18:22:00+07:00	CAM-001	2026-06-17T18:22:00+07:00
ZT-SEED-004	person	504	parking_zone	person_disinfection_zone	2026-06-17T18:19:00+07:00	CAM-001	2026-06-17T18:19:00+07:00
ZT-SEED-005	person	504	person_disinfection_zone	gestation_barn	2026-06-17T18:19:30+07:00	CAM-001	2026-06-17T18:19:30+07:00
ZT-C13665DE410E	person	1	restricted_zone	person_disinfection_zone	2026-06-17T11:54:41.842898+00:00	CAM-001	2026-06-17T11:54:41.842898+00:00
ZT-38A8EEB61CC7	dog	2	restricted_zone	person_disinfection_zone	2026-06-17T11:54:41.842898+00:00	CAM-001	2026-06-17T11:54:41.842898+00:00
ZT-067BE0AE3E83	person	9001	parking_zone	gestation_barn	2026-06-17T20:00:00+07:00	CAM-001	2026-06-17T20:00:00+07:00
ZT-02E39807644E	person	9002	parking_zone	person_disinfection_zone	2026-06-17T20:01:00+07:00	CAM-001	2026-06-17T20:01:00+07:00
ZT-2F8D31AE70DD	person	9002	person_disinfection_zone	gestation_barn	2026-06-17T20:02:00+07:00	CAM-001	2026-06-17T20:02:00+07:00
ZT-EDD566F6B59E	dog	9003	reception_zone	farrowing_barn	2026-06-17T20:03:00+07:00	CAM-001	2026-06-17T20:03:00+07:00
ZT-8BD35016CB6E	vehicle	9004	parking_zone	pig_loading_zone	2026-06-17T20:04:00+07:00	CAM-001	2026-06-17T20:04:00+07:00
ZT-SEED-006	person	601	reception_zone	parking_zone	2026-06-17T19:00:00+07:00	CAM-001	2026-06-17T19:00:00+07:00
ZT-SEED-007	person	601	parking_zone	vehicle_disinfection_zone	2026-06-17T19:01:00+07:00	CAM-001	2026-06-17T19:01:00+07:00
ZT-SEED-008	vehicle	602	parking_zone	vehicle_disinfection_zone	2026-06-17T19:02:00+07:00	CAM-001	2026-06-17T19:02:00+07:00
ZT-9A134A7315D4	person	900	unknown	parking_zone	2026-06-17T22:00:00+07:00	CAM-001	2026-06-17T22:00:00+07:00
ZT-BF5A7BB416F2	person	901	unknown	parking_zone	2026-06-17T22:10:00+07:00	CAM-001	2026-06-17T22:10:00+07:00
ZT-ACFD9F725BD4	person	901	parking_zone	person_disinfection_zone	2026-06-17T22:10:00+07:00	CAM-001	2026-06-17T22:10:00+07:00
ZT-4E5E15A62DEE	person	901	person_disinfection_zone	gestation_barn	2026-06-17T22:10:00+07:00	CAM-001	2026-06-17T22:10:00+07:00
ZT-A1DACC3F8396	dog	801	unknown	parking_zone	2026-06-17T23:01:00+07:00	CAM-001	2026-06-17T23:01:00+07:00
ZT-28470E8DF1D5	dog	802	unknown	gestation_barn	2026-06-17T23:02:00+07:00	CAM-001	2026-06-17T23:02:00+07:00
ZT-8190FD421853	cat	803	unknown	farrowing_barn	2026-06-17T23:03:00+07:00	CAM-001	2026-06-17T23:03:00+07:00
ZT-806D5958D6CD	rat	804	unknown	vet_medicine_storage	2026-06-17T23:04:00+07:00	CAM-001	2026-06-17T23:04:00+07:00
ZT-9080E9068AFE	bird	805	unknown	feed_storage	2026-06-17T23:05:00+07:00	CAM-001	2026-06-17T23:05:00+07:00
ZT-947F62B3D09E	person	9001	gestation_barn	worker_housing	2026-06-17T10:00:00+07:00	CAM-001	2026-06-17T10:00:00+07:00
ZT-4762D652F8EC	person	9001	worker_housing	shower_room	2026-06-17T10:01:00+07:00	CAM-001	2026-06-17T10:01:00+07:00
ZT-AAB3E366D858	person	9001	shower_room	handwash_zone	2026-06-17T10:02:00+07:00	CAM-001	2026-06-17T10:02:00+07:00
ZT-131B394BFD38	person	9001	handwash_zone	boot_disinfection_tray	2026-06-17T10:03:00+07:00	CAM-001	2026-06-17T10:03:00+07:00
ZT-91FE0CB48834	person	9001	boot_disinfection_tray	gestation_barn	2026-06-17T10:04:00+07:00	CAM-001	2026-06-17T10:04:00+07:00
ZT-24882CA094BB	person	9002	gestation_barn	worker_housing	2026-06-17T11:00:00+07:00	CAM-001	2026-06-17T11:00:00+07:00
ZT-81EB05097CC3	person	9002	worker_housing	gestation_barn	2026-06-17T11:05:00+07:00	CAM-001	2026-06-17T11:05:00+07:00
ZT-F6EA88E54156	person	9101	unknown	worker_housing	2026-06-17T14:00:00+07:00	CAM-001	2026-06-17T14:00:00+07:00
ZT-7BA46FC59A5A	person	9101	worker_housing	shower_room	2026-06-17T14:01:00+07:00	CAM-001	2026-06-17T14:01:00+07:00
ZT-87ACB036F355	person	9101	shower_room	handwash_zone	2026-06-17T14:02:00+07:00	CAM-001	2026-06-17T14:02:00+07:00
ZT-3A6ED097039F	person	9101	handwash_zone	boot_disinfection_tray	2026-06-17T14:03:00+07:00	CAM-001	2026-06-17T14:03:00+07:00
ZT-9160BA83D99D	person	9101	boot_disinfection_tray	gestation_barn	2026-06-17T14:04:00+07:00	CAM-001	2026-06-17T14:04:00+07:00
ZT-C26C7F83DB7C	person	9102	unknown	worker_housing	2026-06-17T14:00:00+07:00	CAM-001	2026-06-17T14:00:00+07:00
ZT-4C57A27D064E	person	9102	worker_housing	gestation_barn	2026-06-17T14:01:00+07:00	CAM-001	2026-06-17T14:01:00+07:00
ZT-0C6F7ACFB9A8	person	1001	unknown	worker_housing	2026-06-17T10:01:00	CAM-001	2026-06-17T10:01:00
ZT-A8DBA7504561	person	1001	worker_housing	shower_room	2026-06-17T10:02:00	CAM-001	2026-06-17T10:02:00
ZT-9BB8A02474D2	person	1001	shower_room	handwash_zone	2026-06-17T10:03:00	CAM-001	2026-06-17T10:03:00
ZT-4CCCF77C72DD	person	1001	handwash_zone	boot_disinfection_tray	2026-06-17T10:04:00	CAM-001	2026-06-17T10:04:00
ZT-E2492AF3B437	person	1001	boot_disinfection_tray	gestation_barn	2026-06-17T10:05:00	CAM-001	2026-06-17T10:05:00
ZT-C8B10FC14210	person	1002	unknown	worker_housing	2026-06-17T10:01:00	CAM-001	2026-06-17T10:01:00
ZT-6135C34A1C89	person	1002	worker_housing	gestation_barn	2026-06-17T10:02:00	CAM-001	2026-06-17T10:02:00
ZT-334FE2D11B89	person	1003	unknown	worker_housing	2026-06-17T10:01:00	CAM-001	2026-06-17T10:01:00
ZT-FF71B44A21B2	person	1003	worker_housing	shower_room	2026-06-17T10:02:00	CAM-001	2026-06-17T10:02:00
ZT-7E61EEE5A37A	person	1003	shower_room	boot_disinfection_tray	2026-06-17T10:03:00	CAM-001	2026-06-17T10:03:00
ZT-CDC09FA915D9	person	1003	boot_disinfection_tray	gestation_barn	2026-06-17T10:04:00	CAM-001	2026-06-17T10:04:00
ZT-624EBE129BDB	person	1004	unknown	worker_housing	2026-06-17T10:01:00	CAM-001	2026-06-17T10:01:00
ZT-19CF86479723	person	1004	worker_housing	shower_room	2026-06-17T10:02:00	CAM-001	2026-06-17T10:02:00
ZT-00AA8F02983A	person	1004	shower_room	handwash_zone	2026-06-17T10:03:00	CAM-001	2026-06-17T10:03:00
ZT-5088E40C3624	person	1004	handwash_zone	gestation_barn	2026-06-17T10:04:00	CAM-001	2026-06-17T10:04:00
\.


--
-- Name: ai_models ai_models_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_pkey PRIMARY KEY (id);


--
-- Name: ai_tasks ai_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.ai_tasks
    ADD CONSTRAINT ai_tasks_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: alert_categories alert_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.alert_categories
    ADD CONSTRAINT alert_categories_pkey PRIMARY KEY (code);


--
-- Name: animal_intrusion_policies animal_intrusion_policies_object_type_key; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.animal_intrusion_policies
    ADD CONSTRAINT animal_intrusion_policies_object_type_key UNIQUE (object_type);


--
-- Name: animal_intrusion_policies animal_intrusion_policies_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.animal_intrusion_policies
    ADD CONSTRAINT animal_intrusion_policies_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: biosecurity_rules biosecurity_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.biosecurity_rules
    ADD CONSTRAINT biosecurity_rules_pkey PRIMARY KEY (id);


--
-- Name: camera_health camera_health_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.camera_health
    ADD CONSTRAINT camera_health_pkey PRIMARY KEY (id);


--
-- Name: camera_streams camera_streams_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.camera_streams
    ADD CONSTRAINT camera_streams_pkey PRIMARY KEY (id);


--
-- Name: cameras cameras_ip_address_key; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.cameras
    ADD CONSTRAINT cameras_ip_address_key UNIQUE (ip_address);


--
-- Name: cameras cameras_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.cameras
    ADD CONSTRAINT cameras_pkey PRIMARY KEY (id);


--
-- Name: edge_devices edge_devices_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.edge_devices
    ADD CONSTRAINT edge_devices_pkey PRIMARY KEY (id);


--
-- Name: employees employees_employee_code_key; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_employee_code_key UNIQUE (employee_code);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: event_snapshots event_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.event_snapshots
    ADD CONSTRAINT event_snapshots_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: farm_layout_templates farm_layout_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.farm_layout_templates
    ADD CONSTRAINT farm_layout_templates_pkey PRIMARY KEY (id);


--
-- Name: farm_map_objects farm_map_objects_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.farm_map_objects
    ADD CONSTRAINT farm_map_objects_pkey PRIMARY KEY (id);


--
-- Name: farm_zones farm_zones_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.farm_zones
    ADD CONSTRAINT farm_zones_pkey PRIMARY KEY (id);


--
-- Name: farms farms_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.farms
    ADD CONSTRAINT farms_pkey PRIMARY KEY (id);


--
-- Name: licenses licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_pkey PRIMARY KEY (id);


--
-- Name: notification_gateways notification_gateways_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.notification_gateways
    ADD CONSTRAINT notification_gateways_pkey PRIMARY KEY (id);


--
-- Name: notification_rules notification_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.notification_rules
    ADD CONSTRAINT notification_rules_pkey PRIMARY KEY (id);


--
-- Name: object_tracks object_tracks_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.object_tracks
    ADD CONSTRAINT object_tracks_pkey PRIMARY KEY (id);


--
-- Name: person_tracks person_tracks_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.person_tracks
    ADD CONSTRAINT person_tracks_pkey PRIMARY KEY (id);


--
-- Name: template_zone_definitions template_zone_definitions_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.template_zone_definitions
    ADD CONSTRAINT template_zone_definitions_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist token_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.token_blacklist
    ADD CONSTRAINT token_blacklist_pkey PRIMARY KEY (jti);


--
-- Name: track_workflow_progress track_workflow_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.track_workflow_progress
    ADD CONSTRAINT track_workflow_progress_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: visitors visitors_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.visitors
    ADD CONSTRAINT visitors_pkey PRIMARY KEY (id);


--
-- Name: workflow_steps workflow_steps_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_pkey PRIMARY KEY (id);


--
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- Name: zone_polygons zone_polygons_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.zone_polygons
    ADD CONSTRAINT zone_polygons_pkey PRIMARY KEY (id);


--
-- Name: zone_transitions zone_transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.zone_transitions
    ADD CONSTRAINT zone_transitions_pkey PRIMARY KEY (id);


--
-- Name: ix_ai_models_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_ai_models_id ON public.ai_models USING btree (id);


--
-- Name: ix_ai_tasks_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_ai_tasks_camera_id ON public.ai_tasks USING btree (camera_id);


--
-- Name: ix_ai_tasks_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_ai_tasks_id ON public.ai_tasks USING btree (id);


--
-- Name: ix_alert_categories_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_alert_categories_code ON public.alert_categories USING btree (code);


--
-- Name: ix_animal_intrusion_policies_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_animal_intrusion_policies_id ON public.animal_intrusion_policies USING btree (id);


--
-- Name: ix_animal_intrusion_policies_object_type; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_animal_intrusion_policies_object_type ON public.animal_intrusion_policies USING btree (object_type);


--
-- Name: ix_audit_logs_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);


--
-- Name: ix_audit_logs_user_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_audit_logs_user_id ON public.audit_logs USING btree (user_id);


--
-- Name: ix_biosecurity_rules_category; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_biosecurity_rules_category ON public.biosecurity_rules USING btree (category);


--
-- Name: ix_biosecurity_rules_from_zone; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_biosecurity_rules_from_zone ON public.biosecurity_rules USING btree (from_zone);


--
-- Name: ix_biosecurity_rules_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_biosecurity_rules_id ON public.biosecurity_rules USING btree (id);


--
-- Name: ix_biosecurity_rules_object_type; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_biosecurity_rules_object_type ON public.biosecurity_rules USING btree (object_type);


--
-- Name: ix_biosecurity_rules_rule_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_biosecurity_rules_rule_code ON public.biosecurity_rules USING btree (rule_code);


--
-- Name: ix_biosecurity_rules_to_zone; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_biosecurity_rules_to_zone ON public.biosecurity_rules USING btree (to_zone);


--
-- Name: ix_camera_health_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_camera_health_camera_id ON public.camera_health USING btree (camera_id);


--
-- Name: ix_camera_health_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_camera_health_farm_id ON public.camera_health USING btree (farm_id);


--
-- Name: ix_camera_health_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_camera_health_id ON public.camera_health USING btree (id);


--
-- Name: ix_camera_streams_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_camera_streams_camera_id ON public.camera_streams USING btree (camera_id);


--
-- Name: ix_camera_streams_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_camera_streams_id ON public.camera_streams USING btree (id);


--
-- Name: ix_cameras_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_cameras_farm_id ON public.cameras USING btree (farm_id);


--
-- Name: ix_cameras_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_cameras_id ON public.cameras USING btree (id);


--
-- Name: ix_edge_devices_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_edge_devices_farm_id ON public.edge_devices USING btree (farm_id);


--
-- Name: ix_edge_devices_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_edge_devices_id ON public.edge_devices USING btree (id);


--
-- Name: ix_employees_assigned_zone; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_employees_assigned_zone ON public.employees USING btree (assigned_zone);


--
-- Name: ix_employees_department; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_employees_department ON public.employees USING btree (department);


--
-- Name: ix_employees_employee_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_employees_employee_code ON public.employees USING btree (employee_code);


--
-- Name: ix_employees_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_employees_id ON public.employees USING btree (id);


--
-- Name: ix_event_snapshots_event_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_event_snapshots_event_id ON public.event_snapshots USING btree (event_id);


--
-- Name: ix_event_snapshots_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_event_snapshots_id ON public.event_snapshots USING btree (id);


--
-- Name: ix_events_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_events_camera_id ON public.events USING btree (camera_id);


--
-- Name: ix_events_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_events_farm_id ON public.events USING btree (farm_id);


--
-- Name: ix_events_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_events_id ON public.events USING btree (id);


--
-- Name: ix_events_violation_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_events_violation_code ON public.events USING btree (violation_code);


--
-- Name: ix_farm_layout_templates_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_layout_templates_id ON public.farm_layout_templates USING btree (id);


--
-- Name: ix_farm_map_objects_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_map_objects_id ON public.farm_map_objects USING btree (id);


--
-- Name: ix_farm_zones_biosecurity_level; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_biosecurity_level ON public.farm_zones USING btree (biosecurity_level);


--
-- Name: ix_farm_zones_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_farm_id ON public.farm_zones USING btree (farm_id);


--
-- Name: ix_farm_zones_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_id ON public.farm_zones USING btree (id);


--
-- Name: ix_farm_zones_template_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_template_id ON public.farm_zones USING btree (template_id);


--
-- Name: ix_farm_zones_template_zone_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_template_zone_id ON public.farm_zones USING btree (template_zone_id);


--
-- Name: ix_farm_zones_zone_category; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_zone_category ON public.farm_zones USING btree (zone_category);


--
-- Name: ix_farm_zones_zone_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farm_zones_zone_code ON public.farm_zones USING btree (zone_code);


--
-- Name: ix_farms_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_farms_id ON public.farms USING btree (id);


--
-- Name: ix_licenses_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_licenses_farm_id ON public.licenses USING btree (farm_id);


--
-- Name: ix_licenses_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_licenses_id ON public.licenses USING btree (id);


--
-- Name: ix_notification_gateways_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_notification_gateways_farm_id ON public.notification_gateways USING btree (farm_id);


--
-- Name: ix_notification_gateways_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_notification_gateways_id ON public.notification_gateways USING btree (id);


--
-- Name: ix_notification_rules_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_notification_rules_id ON public.notification_rules USING btree (id);


--
-- Name: ix_object_tracks_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_object_tracks_camera_id ON public.object_tracks USING btree (camera_id);


--
-- Name: ix_object_tracks_current_zone; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_object_tracks_current_zone ON public.object_tracks USING btree (current_zone);


--
-- Name: ix_object_tracks_employee_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_object_tracks_employee_id ON public.object_tracks USING btree (employee_id);


--
-- Name: ix_object_tracks_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_object_tracks_id ON public.object_tracks USING btree (id);


--
-- Name: ix_object_tracks_object_type; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_object_tracks_object_type ON public.object_tracks USING btree (object_type);


--
-- Name: ix_object_tracks_track_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_object_tracks_track_id ON public.object_tracks USING btree (track_id);


--
-- Name: ix_person_tracks_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_person_tracks_camera_id ON public.person_tracks USING btree (camera_id);


--
-- Name: ix_person_tracks_enter_time; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_person_tracks_enter_time ON public.person_tracks USING btree (enter_time);


--
-- Name: ix_person_tracks_track_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_person_tracks_track_id ON public.person_tracks USING btree (track_id);


--
-- Name: ix_person_tracks_zone_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_person_tracks_zone_id ON public.person_tracks USING btree (zone_id);


--
-- Name: ix_template_zone_definitions_biosecurity_level; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_template_zone_definitions_biosecurity_level ON public.template_zone_definitions USING btree (biosecurity_level);


--
-- Name: ix_template_zone_definitions_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_template_zone_definitions_id ON public.template_zone_definitions USING btree (id);


--
-- Name: ix_template_zone_definitions_risk_level; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_template_zone_definitions_risk_level ON public.template_zone_definitions USING btree (risk_level);


--
-- Name: ix_template_zone_definitions_template_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_template_zone_definitions_template_id ON public.template_zone_definitions USING btree (template_id);


--
-- Name: ix_template_zone_definitions_zone_category; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_template_zone_definitions_zone_category ON public.template_zone_definitions USING btree (zone_category);


--
-- Name: ix_template_zone_definitions_zone_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_template_zone_definitions_zone_code ON public.template_zone_definitions USING btree (zone_code);


--
-- Name: ix_token_blacklist_jti; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_token_blacklist_jti ON public.token_blacklist USING btree (jti);


--
-- Name: ix_track_workflow_progress_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_track_workflow_progress_camera_id ON public.track_workflow_progress USING btree (camera_id);


--
-- Name: ix_track_workflow_progress_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_track_workflow_progress_id ON public.track_workflow_progress USING btree (id);


--
-- Name: ix_track_workflow_progress_track_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_track_workflow_progress_track_id ON public.track_workflow_progress USING btree (track_id);


--
-- Name: ix_track_workflow_progress_workflow_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_track_workflow_progress_workflow_id ON public.track_workflow_progress USING btree (workflow_id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_visitors_company; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_visitors_company ON public.visitors USING btree (company);


--
-- Name: ix_visitors_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_visitors_id ON public.visitors USING btree (id);


--
-- Name: ix_visitors_vehicle_plate; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_visitors_vehicle_plate ON public.visitors USING btree (vehicle_plate);


--
-- Name: ix_workflow_steps_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_workflow_steps_id ON public.workflow_steps USING btree (id);


--
-- Name: ix_workflow_steps_step_order; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_workflow_steps_step_order ON public.workflow_steps USING btree (step_order);


--
-- Name: ix_workflow_steps_workflow_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_workflow_steps_workflow_id ON public.workflow_steps USING btree (workflow_id);


--
-- Name: ix_workflow_steps_zone_code; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_workflow_steps_zone_code ON public.workflow_steps USING btree (zone_code);


--
-- Name: ix_workflows_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_workflows_id ON public.workflows USING btree (id);


--
-- Name: ix_workflows_object_type; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_workflows_object_type ON public.workflows USING btree (object_type);


--
-- Name: ix_zone_polygons_biosecurity_level; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_polygons_biosecurity_level ON public.zone_polygons USING btree (biosecurity_level);


--
-- Name: ix_zone_polygons_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_polygons_camera_id ON public.zone_polygons USING btree (camera_id);


--
-- Name: ix_zone_polygons_farm_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_polygons_farm_id ON public.zone_polygons USING btree (farm_id);


--
-- Name: ix_zone_polygons_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_polygons_id ON public.zone_polygons USING btree (id);


--
-- Name: ix_zone_polygons_zone_type; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_polygons_zone_type ON public.zone_polygons USING btree (zone_type);


--
-- Name: ix_zone_transitions_camera_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_camera_id ON public.zone_transitions USING btree (camera_id);


--
-- Name: ix_zone_transitions_cross_time; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_cross_time ON public.zone_transitions USING btree (cross_time);


--
-- Name: ix_zone_transitions_from_zone; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_from_zone ON public.zone_transitions USING btree (from_zone);


--
-- Name: ix_zone_transitions_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_id ON public.zone_transitions USING btree (id);


--
-- Name: ix_zone_transitions_object_type; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_object_type ON public.zone_transitions USING btree (object_type);


--
-- Name: ix_zone_transitions_timestamp; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_timestamp ON public.zone_transitions USING btree ("timestamp");


--
-- Name: ix_zone_transitions_to_zone; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_to_zone ON public.zone_transitions USING btree (to_zone);


--
-- Name: ix_zone_transitions_track_id; Type: INDEX; Schema: public; Owner: ams
--

CREATE INDEX ix_zone_transitions_track_id ON public.zone_transitions USING btree (track_id);


--
-- Name: camera_streams camera_streams_camera_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.camera_streams
    ADD CONSTRAINT camera_streams_camera_id_fkey FOREIGN KEY (camera_id) REFERENCES public.cameras(id);


--
-- Name: event_snapshots event_snapshots_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.event_snapshots
    ADD CONSTRAINT event_snapshots_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: events events_camera_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ams
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_camera_id_fkey FOREIGN KEY (camera_id) REFERENCES public.cameras(id);


--
-- PostgreSQL database dump complete
--

\unrestrict TU7cn3IIwq1G8KtTmDWVY3jZV3VWru5vgtYY6CtvUhhmeLlEQg1X3LlUcxy2ajF

