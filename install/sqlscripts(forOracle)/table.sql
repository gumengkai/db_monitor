prompt PL/SQL Developer Export User Objects for user DBMON@192.168.48.60/PDB1
prompt Created by gmk on 2020Äê1ÔÂ20ÈÕ
set define off
spool table.log

prompt
prompt Creating table SNAP_SHOW
prompt ========================
prompt
create global temporary table DBMON.SNAP_SHOW
(
  id           INTEGER,
  rate         VARCHAR2(32),
  sql_id       VARCHAR2(128),
  sql_exec_cnt VARCHAR2(32),
  val1         VARCHAR2(128),
  val2         VARCHAR2(128),
  val3         VARCHAR2(128),
  val4         VARCHAR2(128),
  val5         VARCHAR2(128),
  val6         VARCHAR2(128),
  val7         VARCHAR2(128),
  val8         VARCHAR2(128),
  val9         VARCHAR2(128),
  snap_type_id INTEGER
)
on commit delete rows;

prompt
prompt Creating table SNAP_SHOW_CONFIG
prompt ===============================
prompt
create global temporary table DBMON.SNAP_SHOW_CONFIG
(
  id         INTEGER not null,
  col1       VARCHAR2(32),
  col2       VARCHAR2(32),
  col3       VARCHAR2(32),
  col4       VARCHAR2(32),
  col5       VARCHAR2(32),
  col6       VARCHAR2(32),
  col7       VARCHAR2(32),
  col8       VARCHAR2(32),
  col9       VARCHAR2(32),
  col10      VARCHAR2(32),
  col11      VARCHAR2(32),
  col12      VARCHAR2(32),
  show_type  VARCHAR2(32),
  show_title VARCHAR2(128),
  inst_info  VARCHAR2(128)
)
on commit delete rows;


prompt Done
spool off
set define on
