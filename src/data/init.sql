CREATE TABLE IF NOT EXISTS datos (

    id SERIAL PRIMARY KEY,

    -- Identificación del cliente
    id_cliente                   VARCHAR(20),

    -- Datos demográficos
    genero                       VARCHAR(10),
    es_adulto_mayor              SMALLINT,
    tiene_pareja                 BOOLEAN,
    tiene_dependientes           BOOLEAN,

    -- Permanencia
    meses_permanencia            INTEGER,

    -- Servicios de telefonía
    tiene_telefono               BOOLEAN,
    tiene_multiples_lineas       VARCHAR(20),

    -- Servicios de internet
    tipo_internet                VARCHAR(15),
    tiene_seguridad_online       VARCHAR(25),
    tiene_backup_online          VARCHAR(25),
    tiene_proteccion_dispositivo VARCHAR(25),
    tiene_soporte_tecnico        VARCHAR(25),
    tiene_streaming_tv           VARCHAR(25),
    tiene_streaming_peliculas    VARCHAR(25),

    -- Contrato y facturación
    tipo_contrato                VARCHAR(20),
    facturacion_sin_papel        BOOLEAN,
    metodo_pago                  VARCHAR(30),
    cargo_mensual                NUMERIC,
    cargo_total                  NUMERIC,

    -- Target
    abandono_servicio            BOOLEAN,

    -- Auditoría
    fecha_carga                  TIMESTAMP       DEFAULT NOW()
);