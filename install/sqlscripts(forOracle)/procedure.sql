prompt PL/SQL Developer Export User Objects for user DBMON@192.168.48.60/PDB1
prompt Created by gmk on 2020Äê1ÔÂ20ÈÕ
set define off
spool procedure&function.log

prompt
prompt Creating function FUNCAS_FORMAT_NUM_OUTPUT
prompt ==========================================
prompt
create or replace function dbmon.funcas_format_num_output(v_number  in number,
                                                    v_type in varchar2)
  return varchar2 is
  v_out_number varchar2(30);
begin
if v_type='Time-mic' then

if length(v_number)>=9 then
v_out_number:=trunc(v_number/1000000)||'s';
elsif length(v_number)<9 and length(v_number)>=7 then
v_out_number:=round(v_number/1000000,2)||'s';
elsif length(v_number)<7 and length(v_number)>=5 then
v_out_number:=trunc(v_number/1000)||'ms';
elsif length(v_number)<5 then
v_out_number:=round(v_number/1000,2)||'ms';
end if;

elsif v_type='Time-s' then
null;
elsif v_type='Times' then
if length(v_number)>=9 then
v_out_number:=trunc(v_number/1000000)||'M';
elsif length(v_number)<9 and length(v_number)>=7 then
v_out_number:=round(v_number/1000000,2)||'M';
elsif length(v_number)<7 and length(v_number)>=5 then
v_out_number:=trunc(v_number/1000)||'K';
elsif length(v_number)<5 and length(v_number)>3 then
v_out_number:=round(v_number/1000,2)||'K';
elsif length(v_number)<=3 then
v_out_number:=v_number;
end if;
elsif v_type='Bytes' then

if length(v_number)>=15 then
v_out_number:=trunc(v_number/1024/1024/1024/1024)||'TB';
elsif length(v_number)>12 and length(v_number)<15 then
v_out_number:=round(v_number/1024/1024/1024/1024,2)||'TB';
elsif length(v_number)=12 then
v_out_number:=trunc(v_number/1024/1024/1024)||'GB';
elsif length(v_number)>9 and length(v_number)<12 then
v_out_number:=round(v_number/1024/1024/1024,2)||'GB';
elsif length(v_number)=9 then
v_out_number:=trunc(v_number/1024/1024)||'MB';
elsif length(v_number)<9 and length(v_number)>=7 then
v_out_number:=round(v_number/1024/1024,2)||'MB';
elsif length(v_number)<7 and length(v_number)>=5 then
v_out_number:=trunc(v_number/1024)||'KB';
elsif length(v_number)<5 then
v_out_number:=round(v_number/1000,2)||'KB';
end if;

end if;

if substr(v_out_number,0,1)='.' then
v_out_number:='0'||v_out_number;
end if;

return(v_out_number);
end;
/

prompt
prompt Creating function REGEXP_NUMCOUNT_CAS
prompt =====================================
prompt
create or replace function dbmon.regexp_numcount_cas(strstr  in varchar2,
                                                  pattern in varchar2 default '[[:digit:]]{1,}')
  return number is
  result_count number;
  j            number;
begin
  j            := 1;
  result_count := 0;
  while regexp_substr(strstr, pattern, 1, j, 'i') is not null loop
    j            := j + 1;
    result_count := result_count + 1;
  end loop;
  return(result_count);
end;
/

prompt
prompt Creating procedure PROCAS_719_STANDARD_ROW_OUTPUT
prompt =================================================
prompt
create or replace procedure dbmon.procas_719_standard_row_output(title_name in varchar2,
column_num in number,
column_len_str in varchar2,
sep_flag in varchar2,
show_text in varchar2) is
v_title_name varchar2(100);
v_column_num number;
v_column_len number;
v_sep_flag varchar2(10);
v_show_text varchar2(1000);
v_output varchar2(1000);
v_column_len_str varchar2(100);
v_column_len_char varchar2(20);
v_length number;
v_char varchar2(100);
v_flag varchar2(100);
v_default_len number;
v_add_range number;
v_default_text_len number;


begin
v_add_range:=2;
v_default_len:=30;
v_default_text_len:=60;
v_title_name:=title_name;
v_column_num:=column_num;
v_column_len_str:=column_len_str;
v_sep_flag:=sep_flag;
v_show_text:=show_text;
v_column_len:=v_default_len;

if title_name is not null then

v_char:=v_title_name;
v_length:=v_column_len-length(v_char);

if v_length<0 then
v_char:=substr(v_char,0,v_column_len-1);
end if;
v_char:=rpad(v_char,v_column_len,' ');
v_output:=v_output||v_char;
end if;

for i in 1..column_num loop
v_char:='';
if i=1 and regexp_substr(v_show_text,v_sep_flag) is not null then
v_char:=substr(v_show_text,0,instr(v_show_text,v_sep_flag,1,i)-1);
v_column_len_char:=substr(v_column_len_str,0,instr(v_column_len_str,v_sep_flag,1,i)-1);
elsif i=1 and regexp_substr(v_show_text,v_sep_flag) is null then
v_char:=v_show_text;
v_column_len_char:=v_column_len_str;
elsif i=column_num then
v_char:=substr(v_show_text,instr(v_show_text,v_sep_flag,1,i-1)+1);
v_column_len_char:=substr(v_column_len_str,instr(v_column_len_str,v_sep_flag,1,i-1)+1);

else
v_char:=substr(v_show_text,instr(v_show_text,v_sep_flag,1,i-1)+1,instr(v_show_text,v_sep_flag,1,i)-(instr(v_show_text,v_sep_flag,1,i-1)+1));
v_column_len_char:=substr(v_column_len_str,instr(v_column_len_str,v_sep_flag,1,i-1)+1,instr(v_column_len_str,v_sep_flag,1,i)-(instr(v_column_len_str,v_sep_flag,1,i-1)+1));

end if;
if v_char is null then
v_char:=' ';
end if;

if length(v_char)<v_default_text_len then
if regexp_substr(v_column_len_char,'^[0-9]*$') is not null then
v_column_len:=to_number(v_column_len_char)+v_add_range;
else
v_column_len:=v_default_len;
end if;
elsif length(v_char) >=v_default_text_len then
v_column_len:=v_default_text_len;
end if;

v_length:=v_column_len-length(v_char);
if v_length<=0 then
v_char:=substr(v_char,0,v_column_len-v_add_range);
v_char:=rpad(v_char,v_column_len,' ');
end if;
v_char:=rpad(v_char,v_column_len,' ');
v_output:=v_output||v_char;
end loop;

dbms_output.put_line(v_output);

end;
/

prompt
prompt Creating procedure PRO_TOP_CPU_SQL
prompt ==================================
prompt
create or replace procedure dbmon.pro_top_cpu_sql as
  v_value        number;
  v_number       number;
  v_flag1        varchar2(200);
  v_flag2        varchar2(200);
  v_output1      varchar2(200);
  v_length       number;
  v_n            number;
  v_per_len      number;
  v_remark_len   number default 30;
  v_type_len     number default 7;
  v_max_snap_id  number;
  v_snap_show_id number default 1;
  v_exec_total   number;
  v_exec_rownum  number default 10;
  v_snap_ago     number default 8;
  v_titel_len    number default 10;
  v_col_snap_id1 number;
  v_col_title1   varchar2(30);
  v_col_flag1    number;
  v_col_snap_id2 number;
  v_col_title2   varchar2(30);
  v_col_flag2    number;
  v_col_snap_id3 number;
  v_col_title3   varchar2(30);
  v_col_flag3    number;
  v_col_snap_id4 number;
  v_col_title4   varchar2(30);
  v_col_flag4    number;
  v_col_snap_id5 number;
  v_col_title5   varchar2(30);
  v_col_flag5    number;
  v_col_snap_id6 number;
  v_col_title6   varchar2(30);
  v_col_flag6    number;
  v_col_snap_id7 number;
  v_col_title7   varchar2(30);
  v_col_flag7    number;
  v_sql_len      number default 14;
  v_remark       varchar2(100);
  v_p_schema     varchar2(100);
  v_first_load   varchar2(38);
  v_col_num1     number;
  v_col_exec1    number;
  v_col_num2     number;
  v_col_num3     number;
  v_col_num4     number;
  v_col_num5     number;
  v_col_num6     number;
  v_col_num7     number;
  v_col_show1    varchar2(30);
  v_col_eshow1   varchar2(30);
  v_col_show2    varchar2(30);
  v_col_show3    varchar2(30);
  v_col_show4    varchar2(30);
  v_col_show5    varchar2(30);
  v_col_show6    varchar2(30);
  v_col_show7    varchar2(30);
  v_count        number;
  v_max_exec     number;
  v_show_exec    number;
  v_sql_used     number;
  v_show_per     varchar2(10);
  v_now_per      varchar2(10);
  v_sql_text     varchar2(30000);
  v_sql_rule     varchar2(100) default 'ALTER|UPDATE|INSERT|DELETE|SELECT';
  v_sql_type     varchar2(20);
begin
  v_col_flag1 := 0;
  v_col_flag2 := 0;
  v_col_flag3 := 0;
  v_col_flag4 := 0;
  v_col_flag5 := 0;
  v_col_flag6 := 0;
  v_col_flag7 := 0;
  v_per_len   := 7;
  v_n         := 80;
  v_output1   := '  Top SQLStat Checking Starting  ';
  v_length    := trunc((v_n - length(v_output1)) / 2);
  v_flag1     := lpad('*', v_length, '*');

  dbms_output.put_line(v_flag1 || v_output1 || v_flag1);
  dbms_output.put_line(' ');
  delete from  snap_show_config where id=1;
  delete from snap_show where snap_type_id = 1;

  for cur_inst in (select host_name,
                          inst_id,
                          instance_name,
                          version,
                          startup_time
                     from gv$instance) loop

    dbms_output.put_line('Instance >>( ' || cur_inst.inst_id ||
                         ' )<< Hostname: ' || cur_inst.host_name ||
                         ' Startup: ' ||
                         to_char(cur_inst.startup_time, 'yyyymmdd hh24:mi') ||
                         ' Version: ' || cur_inst.version);

    for cur_snap_id in (select snap_id, end_interval_time, rownum row_num
                          from (select snap_id, end_interval_time
                                  from dba_hist_snapshot
                                 where end_interval_time >
                                       sysdate - v_snap_ago
                                   and instance_number = cur_inst.inst_id
                                 order by snap_id desc)) loop
      if cur_snap_id.row_num <= 4 then
        if cur_snap_id.row_num = 1 then
          v_col_snap_id1 := cur_snap_id.snap_id;
          v_col_title1   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 2 then
          v_col_snap_id2 := cur_snap_id.snap_id;
          v_col_title2   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 3 then
          v_col_snap_id3 := cur_snap_id.snap_id;
          v_col_title3   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 4 then
          v_col_snap_id4 := cur_snap_id.snap_id;
          v_col_title4   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        end if;
      else
        if cur_snap_id.end_interval_time < sysdate - 3 / 48 and
           v_col_flag5 = 0 then
          v_col_snap_id5 := cur_snap_id.snap_id;
          v_col_title5   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag5    := 1;
        elsif cur_snap_id.end_interval_time < sysdate - 1 and
              v_col_flag6 = 0 then
          v_col_snap_id6 := cur_snap_id.snap_id;
          v_col_title6   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag6    := 1;
        elsif cur_snap_id.end_interval_time < sysdate - v_snap_ago + 1 and
              v_col_flag7 = 0 then
          v_col_snap_id7 := cur_snap_id.snap_id;
          v_col_title7   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag7    := 1;
        end if;
      end if;
    end loop;

    if cur_inst.inst_id = 1 then

      v_output1 := '  Top SQLStat - Cpu Time ';
      v_length  := trunc((v_n - length(v_output1)) / 2);
      v_flag1   := lpad('*', v_length, '*');

      dbms_output.put_line(v_flag1 || v_output1 || v_flag1);
      dbms_output.put_line(' ');
    end if;

    select sum(cpu_time_delta)
      into v_max_exec
      from dba_hist_sqlstat a
     where a.snap_id = v_col_snap_id1
       and a.instance_number = cur_inst.inst_id;

    select sum(cpu_time_delta)
      into v_show_exec
      from (select cpu_time_delta
              from dba_hist_sqlstat a
             where a.snap_id = v_col_snap_id1
               and a.instance_number = cur_inst.inst_id
             order by a.cpu_time_delta desc)
     where rownum <= v_exec_rownum;

    v_show_per := round(v_show_exec / v_max_exec * 100, 2) || '%';

    procas_719_standard_row_output(null,
                                   10,
                                   v_sql_len + v_per_len * 2 || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_type_len || ',' ||
                                   v_remark_len,
                                   ',',
                                   '(' || v_show_per || ')Sql Id' || ',' ||
                                   v_col_title1 || ',' || v_col_title2 || ',' ||
                                   v_col_title3 || ',' || v_col_title4 || ',' ||
                                   v_col_title5 || ',' || v_col_title6 || ',' ||
                                   v_col_title7 || ',' || 'SqlType' || ',' ||
                                   'Remark');
    delete from snap_show_config where show_type = 'TOL SQL';
    insert into snap_show_config
      (id,
       col1,
       col2,
       col3,
       col4,
       col5,
       col6,
       col7,
       col8,
       col9,
       col10,
       col11,
       col12,
       show_type,
       show_title,
       inst_info)
    values
      (1,
       v_show_per,
       'Sql Id',
       'SQL Exec count',
       v_col_title1,
       v_col_title2,
       v_col_title3,
       v_col_title4,
       v_col_title5,
       v_col_title6,
       v_col_title7,
       'SqlType',
       'Remark',
       'TOL SQL',
       v_output1,
       'Instance >>( ' || cur_inst.inst_id || ' )<< Hostname: ' ||
       cur_inst.host_name || ' Startup: ' ||
       to_char(cur_inst.startup_time, 'yyyymmdd hh24:mi') || ' Version: ' ||
       cur_inst.version);
    delete from snap_show where snap_type_id = 1;
    for cur_exec in (select sql_id
                       from (select sql_id
                               from dba_hist_sqlstat a
                              where a.snap_id = v_col_snap_id1
                                and a.instance_number = cur_inst.inst_id
                              order by a.cpu_time_delta desc)
                      where rownum <= v_exec_rownum) loop

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id1
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select sum(cpu_time_delta),
               trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END)),
               (CASE
                 WHEN sum(executions_delta) = 0 THEN
                  1
                 else
                  sum(executions_delta)
               END)
          into v_sql_used, v_col_num1, v_col_exec1
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id1
           and instance_number = cur_inst.inst_id;
        v_col_show1  := funcas_format_num_output(v_col_num1, 'Time-mic');
        v_col_eshow1 := funcas_format_num_output(v_col_exec1, 'Times');

        select count(*)
          into v_count
          from gv$sql
         where sql_id = cur_exec.sql_id
           and inst_id = cur_inst.inst_id;
        if v_count <> 0 then
          select min(parsing_schema_name), min(first_load_time)
            into v_p_schema, v_first_load
            from gv$sql
           where sql_id = cur_exec.sql_id
             and inst_id = cur_inst.inst_id;
          v_remark := v_p_schema || '- ' ||
                      trunc(sysdate -
                            to_date(v_first_load, 'yyyy-mm-dd/hh24:mi:ss')) || 'D';
        else
          v_remark := 'UNKNOW';
        end if;

      else
        v_col_num1  := 0;
        v_col_exec1 := 0;
        v_col_show1 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id2
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END))
          into v_col_num2
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id2
           and instance_number = cur_inst.inst_id;
        v_col_show2 := funcas_format_num_output(v_col_num2, 'Time-mic');
      else
        v_col_num2  := 0;
        v_col_show2 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id3
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END))
          into v_col_num3
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id3
           and instance_number = cur_inst.inst_id;
        v_col_show3 := funcas_format_num_output(v_col_num3, 'Time-mic');
      else
        v_col_num3  := 0;
        v_col_show3 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id4
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END))
          into v_col_num4
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id4
           and instance_number = cur_inst.inst_id;
        v_col_show4 := funcas_format_num_output(v_col_num4, 'Time-mic');
      else
        v_col_num4  := 0;
        v_col_show4 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id5
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END))
          into v_col_num5
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id5
           and instance_number = cur_inst.inst_id;
        v_col_show5 := funcas_format_num_output(v_col_num5, 'Time-mic');
      else
        v_col_num5  := 0;
        v_col_show5 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id6
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END))
          into v_col_num6
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id6
           and instance_number = cur_inst.inst_id;
        v_col_show6 := funcas_format_num_output(v_col_num6, 'Time-mic');
      else
        v_col_num6  := 0;
        v_col_show6 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id7
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(cpu_time_delta) / (CASE
                                              WHEN sum(executions_delta) = 0 THEN
                                               1
                                              else
                                               sum(executions_delta)
                                            END))
          into v_col_num7
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id7
           and instance_number = cur_inst.inst_id;
        v_col_show7 := funcas_format_num_output(v_col_num7, 'Time-mic');
      else
        v_col_num7  := 0;
        v_col_show7 := 0;
      end if;

      v_now_per := round(v_sql_used / v_max_exec * 100, 2) || '%';

      select count(*)
        into v_count
        from dba_hist_sqltext
       where sql_id = cur_exec.sql_id;
      if v_count <> 0 then
        select regexp_substr(upper(sql_text), v_sql_rule, 1, 1)
          into v_sql_text
          from dba_hist_sqltext
         where sql_id = cur_exec.sql_id;
        if v_sql_text is null then
          v_sql_text := 'UNKNOW';
        end if;
      else
        v_sql_text := 'UNKNOW';
      end if;

      procas_719_standard_row_output(null,
                                     10,
                                     v_sql_len + v_per_len * 2 || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_type_len || ',' ||
                                     v_remark_len,
                                     ',',
                                     '(' || v_now_per || ')' ||
                                     cur_exec.sql_id || '(' || v_col_eshow1 || ')' || ',' ||
                                     v_col_show1 || ',' || v_col_show2 || ',' ||
                                     v_col_show3 || ',' || v_col_show4 || ',' ||
                                     v_col_show5 || ',' || v_col_show6 || ',' ||
                                     v_col_show7 || ',' || v_sql_text || ',' ||
                                     v_remark);
      insert into snap_show
        (id,
         rate,
         sql_id,
         sql_exec_cnt,
         val1,
         val2,
         val3,
         val4,
         val5,
         val6,
         val7,
         val8,
         val9,
         snap_type_id)
      values
        (v_snap_show_id,
         v_now_per,
         cur_exec.sql_id,
         v_col_eshow1,
         v_col_show1,
         v_col_show2,
         v_col_show3,
         v_col_show4,
         v_col_show5,
         v_col_show6,
         v_col_show7,
         v_sql_text,
         v_remark,
         1);
      v_snap_show_id := v_snap_show_id + 1;
    end loop;

  /*
    v_output1:='  Top SQLStat - Cpu Used  ';
    v_length:=trunc((v_n-length(v_output1))/2);
    v_flag1:=lpad('*',v_length,'*');

    dbms_output.put_line(v_flag1||v_output1||v_flag1);
    dbms_output.put_line(' ');


    v_output1:='  Top SQLStat - Elapsed Time  ';
    v_length:=trunc((v_n-length(v_output1))/2);
    v_flag1:=lpad('*',v_length,'*');

    dbms_output.put_line(v_flag1||v_output1||v_flag1);
    dbms_output.put_line(' ');


    v_output1:='  Top SQLStat - Logic Read  ';
    v_length:=trunc((v_n-length(v_output1))/2);
    v_flag1:=lpad('*',v_length,'*');

    dbms_output.put_line(v_flag1||v_output1||v_flag1);
    dbms_output.put_line(' ');


    v_output1:='  Top SQLStat - Physical Read Bytes ';
    v_length:=trunc((v_n-length(v_output1))/2);
    v_flag1:=lpad('*',v_length,'*');

    dbms_output.put_line(v_flag1||v_output1||v_flag1);
    dbms_output.put_line(' ');
    */

  end loop;

  v_output1 := '  End Top SQLStat Check  ';
  v_length  := trunc((v_n - length(v_output1)) / 2);
  v_flag1   := lpad('*', v_length, '*');
  v_flag2   := lpad('*', v_n - v_length - length(v_output1), '*');

  dbms_output.put_line(v_flag1 || v_output1 || v_flag2);
  dbms_output.put_line(' ');

end;
/

prompt
prompt Creating procedure PRO_TOP_LOGIC_SQL
prompt ====================================
prompt
create or replace procedure dbmon.pro_top_logic_sql as
  v_value      number;
  v_number     number;
  v_flag1      varchar2(200);
  v_flag2      varchar2(200);
  v_output1    varchar2(200);
  v_length     number;
  v_n          number;
  v_per_len    number;
  v_remark_len number default 30;
  v_type_len   number default 7;

  v_max_snap_id  number;
  v_snap_show_id number default 1;
  v_exec_total   number;
  v_exec_rownum  number default 10;
  v_snap_ago     number default 8;
  v_titel_len    number default 10;
  v_col_snap_id1 number;
  v_col_title1   varchar2(30);
  v_col_flag1    number;
  v_col_snap_id2 number;
  v_col_title2   varchar2(30);
  v_col_flag2    number;
  v_col_snap_id3 number;
  v_col_title3   varchar2(30);
  v_col_flag3    number;
  v_col_snap_id4 number;
  v_col_title4   varchar2(30);
  v_col_flag4    number;
  v_col_snap_id5 number;
  v_col_title5   varchar2(30);
  v_col_flag5    number;
  v_col_snap_id6 number;
  v_col_title6   varchar2(30);
  v_col_flag6    number;
  v_col_snap_id7 number;
  v_col_title7   varchar2(30);
  v_col_flag7    number;
  v_sql_len      number default 14;
  v_remark       varchar2(100);
  v_p_schema     varchar2(100);
  v_first_load   varchar2(38);

  v_col_num1  number;
  v_col_exec1 number;
  v_col_num2  number;
  v_col_num3  number;
  v_col_num4  number;
  v_col_num5  number;
  v_col_num6  number;
  v_col_num7  number;

  v_col_show1  varchar2(30);
  v_col_eshow1 varchar2(30);
  v_col_show2  varchar2(30);
  v_col_show3  varchar2(30);
  v_col_show4  varchar2(30);
  v_col_show5  varchar2(30);
  v_col_show6  varchar2(30);
  v_col_show7  varchar2(30);

  v_count     number;
  v_max_exec  number;
  v_show_exec number;
  v_sql_used  number;
  v_show_per  varchar2(10);
  v_now_per   varchar2(10);
  v_sql_text  varchar2(30000);
  v_sql_rule  varchar2(100) default 'ALTER|UPDATE|INSERT|DELETE|SELECT';
  v_sql_type  varchar2(20);

begin

  v_col_flag1 := 0;
  v_col_flag2 := 0;
  v_col_flag3 := 0;
  v_col_flag4 := 0;
  v_col_flag5 := 0;
  v_col_flag6 := 0;
  v_col_flag7 := 0;

  v_per_len := 7;
  v_n       := 80;
  v_output1 := '  Top SQLStat Checking Starting  ';
  v_length  := trunc((v_n - length(v_output1)) / 2);
  v_flag1   := lpad('*', v_length, '*');

  dbms_output.put_line(v_flag1 || v_output1 || v_flag1);
  dbms_output.put_line(' ');

  delete from snap_show_config where id = 2;
  delete from snap_show where snap_type_id = 2;

  for cur_inst in (select host_name,
                          inst_id,
                          instance_name,
                          version,
                          startup_time
                     from gv$instance) loop

    dbms_output.put_line('Instance >>( ' || cur_inst.inst_id ||
                         ' )<< Hostname: ' || cur_inst.host_name ||
                         ' Startup: ' ||
                         to_char(cur_inst.startup_time, 'yyyymmdd hh24:mi') ||
                         ' Version: ' || cur_inst.version);

    for cur_snap_id in (select snap_id, end_interval_time, rownum row_num
                          from (select snap_id, end_interval_time
                                  from dba_hist_snapshot
                                 where end_interval_time >
                                       sysdate - v_snap_ago
                                   and instance_number = cur_inst.inst_id
                                 order by snap_id desc)) loop
      if cur_snap_id.row_num <= 4 then
        if cur_snap_id.row_num = 1 then
          v_col_snap_id1 := cur_snap_id.snap_id;
          v_col_title1   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 2 then
          v_col_snap_id2 := cur_snap_id.snap_id;
          v_col_title2   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 3 then
          v_col_snap_id3 := cur_snap_id.snap_id;
          v_col_title3   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 4 then
          v_col_snap_id4 := cur_snap_id.snap_id;
          v_col_title4   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        end if;
      else
        if cur_snap_id.end_interval_time < sysdate - 3 / 48 and
           v_col_flag5 = 0 then
          v_col_snap_id5 := cur_snap_id.snap_id;
          v_col_title5   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag5    := 1;
        elsif cur_snap_id.end_interval_time < sysdate - 1 and
              v_col_flag6 = 0 then
          v_col_snap_id6 := cur_snap_id.snap_id;
          v_col_title6   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag6    := 1;
        elsif cur_snap_id.end_interval_time < sysdate - v_snap_ago + 1 and
              v_col_flag7 = 0 then
          v_col_snap_id7 := cur_snap_id.snap_id;
          v_col_title7   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag7    := 1;
        end if;
      end if;
    end loop;

    if cur_inst.inst_id = 1 then

      v_output1 := '  Top SQLStat - Logic Read ';
      v_length  := trunc((v_n - length(v_output1)) / 2);
      v_flag1   := lpad('*', v_length, '*');

      dbms_output.put_line(v_flag1 || v_output1 || v_flag1);
      dbms_output.put_line(' ');
    end if;

    select sum(buffer_gets_delta + disk_reads_delta)
      into v_max_exec
      from dba_hist_sqlstat a
     where a.snap_id = v_col_snap_id1
       and a.instance_number = cur_inst.inst_id;

    select sum(buffer_gets_delta + disk_reads_delta)
      into v_show_exec
      from (select buffer_gets_delta, disk_reads_delta
              from dba_hist_sqlstat a
             where a.snap_id = v_col_snap_id1
               and a.instance_number = cur_inst.inst_id
             order by buffer_gets_delta + disk_reads_delta desc)
     where rownum <= v_exec_rownum;

    v_show_per := round(v_show_exec / v_max_exec * 100, 2) || '%';

    procas_719_standard_row_output(null,
                                   10,
                                   v_sql_len + v_per_len * 2 || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_type_len || ',' ||
                                   v_remark_len,
                                   ',',
                                   '(' || v_show_per || ')Sql Id' || ',' ||
                                   v_col_title1 || ',' || v_col_title2 || ',' ||
                                   v_col_title3 || ',' || v_col_title4 || ',' ||
                                   v_col_title5 || ',' || v_col_title6 || ',' ||
                                   v_col_title7 || ',' || 'SqlType' || ',' ||
                                   'Remark');
    insert into snap_show_config
      (id,
       col1,
       col2,
       col3,
       col4,
       col5,
       col6,
       col7,
       col8,
       col9,
       col10,
       col11,
       col12,
       show_type,
       show_title,
       inst_info)
    values
      (2,
       v_show_per,
       'Sql Id',
       'SQL Exec count',
       v_col_title1,
       v_col_title2,
       v_col_title3,
       v_col_title4,
       v_col_title5,
       v_col_title6,
       v_col_title7,
       'SqlType',
       'Remark',
       'TOL SQL',
       v_output1,
       'Instance >>( ' || cur_inst.inst_id || ' )<< Hostname: ' ||
       cur_inst.host_name || ' Startup: ' ||
       to_char(cur_inst.startup_time, 'yyyymmdd hh24:mi') || ' Version: ' ||
       cur_inst.version);

    for cur_exec in (select sql_id
                       from (select sql_id
                               from dba_hist_sqlstat a
                              where a.snap_id = v_col_snap_id1
                                and a.instance_number = cur_inst.inst_id
                              order by buffer_gets_delta + disk_reads_delta desc)
                      where rownum <= v_exec_rownum) loop

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id1
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select sum(buffer_gets_delta + disk_reads_delta),
               trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END)),
               (CASE
                 WHEN sum(executions_delta) = 0 THEN
                  1
                 else
                  sum(executions_delta)
               END)
          into v_sql_used, v_col_num1, v_col_exec1
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id1
           and instance_number = cur_inst.inst_id;
        v_col_show1  := funcas_format_num_output(v_col_num1, 'Times');
        v_col_eshow1 := funcas_format_num_output(v_col_exec1, 'Times');

        select count(*)
          into v_count
          from gv$sql
         where sql_id = cur_exec.sql_id
           and inst_id = cur_inst.inst_id;
        if v_count <> 0 then
          select min(parsing_schema_name), min(first_load_time)
            into v_p_schema, v_first_load
            from gv$sql
           where sql_id = cur_exec.sql_id
             and inst_id = cur_inst.inst_id;
          v_remark := v_p_schema || '-' ||
                      trunc(sysdate -
                            to_date(v_first_load, 'yyyy-mm-dd/hh24:mi:ss')) || 'D';
        else
          v_remark := 'UNKNOW';
        end if;

      else
        v_col_num1  := 0;
        v_col_exec1 := 0;
        v_col_show1 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id2
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num2
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id2
           and instance_number = cur_inst.inst_id;
        v_col_show2 := funcas_format_num_output(v_col_num2, 'Times');
      else
        v_col_num2  := 0;
        v_col_show2 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id3
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num3
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id3
           and instance_number = cur_inst.inst_id;
        v_col_show3 := funcas_format_num_output(v_col_num3, 'Times');
      else
        v_col_num3  := 0;
        v_col_show3 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id4
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num4
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id4
           and instance_number = cur_inst.inst_id;
        v_col_show4 := funcas_format_num_output(v_col_num4, 'Times');
      else
        v_col_num4  := 0;
        v_col_show4 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id5
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num5
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id5
           and instance_number = cur_inst.inst_id;
        v_col_show5 := funcas_format_num_output(v_col_num5, 'Times');
      else
        v_col_num5  := 0;
        v_col_show5 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id6
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num6
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id6
           and instance_number = cur_inst.inst_id;
        v_col_show6 := funcas_format_num_output(v_col_num6, 'Times');
      else
        v_col_num6  := 0;
        v_col_show6 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id7
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(buffer_gets_delta + disk_reads_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num7
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id7
           and instance_number = cur_inst.inst_id;
        v_col_show7 := funcas_format_num_output(v_col_num7, 'Times');
      else
        v_col_num7  := 0;
        v_col_show7 := 0;
      end if;

      v_now_per := round(v_sql_used / v_max_exec * 100, 2) || '%';

      select count(*)
        into v_count
        from dba_hist_sqltext
       where sql_id = cur_exec.sql_id;
      if v_count <> 0 then
        select regexp_substr(upper(sql_text), v_sql_rule, 1, 1)
          into v_sql_text
          from dba_hist_sqltext
         where sql_id = cur_exec.sql_id;
        if v_sql_text is null then
          v_sql_text := 'UNKNOW';
        end if;
      else
        v_sql_text := 'UNKNOW';
      end if;

      procas_719_standard_row_output(null,
                                     10,
                                     v_sql_len + v_per_len * 2 || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_type_len || ',' ||
                                     v_remark_len,
                                     ',',
                                     '(' || v_now_per || ')' ||
                                     cur_exec.sql_id || '(' || v_col_eshow1 || ')' || ',' ||
                                     v_col_show1 || ',' || v_col_show2 || ',' ||
                                     v_col_show3 || ',' || v_col_show4 || ',' ||
                                     v_col_show5 || ',' || v_col_show6 || ',' ||
                                     v_col_show7 || ',' || v_sql_text || ',' ||
                                     v_remark);
      insert into snap_show
        (id,
         rate,
         sql_id,
         sql_exec_cnt,
         val1,
         val2,
         val3,
         val4,
         val5,
         val6,
         val7,
         val8,
         val9,
         snap_type_id)
      values
        (v_snap_show_id,
         v_now_per,
         cur_exec.sql_id,
         v_col_eshow1,
         v_col_show1,
         v_col_show2,
         v_col_show3,
         v_col_show4,
         v_col_show5,
         v_col_show6,
         v_col_show7,
         v_sql_text,
         v_remark,
         2);
      v_snap_show_id := v_snap_show_id + 1;

    end loop;

  /*
      v_output1:='  Top SQLStat - Cpu Used  ';
      v_length:=trunc((v_n-length(v_output1))/2);
      v_flag1:=lpad('*',v_length,'*');

      dbms_output.put_line(v_flag1||v_output1||v_flag1);
      dbms_output.put_line(' ');


      v_output1:='  Top SQLStat - Elapsed Time  ';
      v_length:=trunc((v_n-length(v_output1))/2);
      v_flag1:=lpad('*',v_length,'*');

      dbms_output.put_line(v_flag1||v_output1||v_flag1);
      dbms_output.put_line(' ');


      v_output1:='  Top SQLStat - Logic Read  ';
      v_length:=trunc((v_n-length(v_output1))/2);
      v_flag1:=lpad('*',v_length,'*');

      dbms_output.put_line(v_flag1||v_output1||v_flag1);
      dbms_output.put_line(' ');


      v_output1:='  Top SQLStat - Physical Read Bytes ';
      v_length:=trunc((v_n-length(v_output1))/2);
      v_flag1:=lpad('*',v_length,'*');

      dbms_output.put_line(v_flag1||v_output1||v_flag1);
      dbms_output.put_line(' ');
      */

  end loop;

  v_output1 := '  End Top SQLStat Check  ';
  v_length  := trunc((v_n - length(v_output1)) / 2);
  v_flag1   := lpad('*', v_length, '*');
  v_flag2   := lpad('*', v_n - v_length - length(v_output1), '*');

  dbms_output.put_line(v_flag1 || v_output1 || v_flag2);
  dbms_output.put_line(' ');

end;
/

prompt
prompt Creating procedure PRO_TOP_PHYS_SQL
prompt ===================================
prompt
create or replace procedure dbmon.pro_top_phys_sql as
  v_value      number;
  v_number     number;
  v_flag1      varchar2(200);
  v_flag2      varchar2(200);
  v_output1    varchar2(200);
  v_length     number;
  v_n          number;
  v_per_len    number;
  v_remark_len number default 30;
  v_type_len   number default 7;

  v_max_snap_id  number;
  v_snap_show_id number default 1;
  v_exec_total   number;
  v_exec_rownum  number default 10;
  v_snap_ago     number default 8;
  v_titel_len    number default 10;
  v_col_snap_id1 number;
  v_col_title1   varchar2(30);
  v_col_flag1    number;
  v_col_snap_id2 number;
  v_col_title2   varchar2(30);
  v_col_flag2    number;
  v_col_snap_id3 number;
  v_col_title3   varchar2(30);
  v_col_flag3    number;
  v_col_snap_id4 number;
  v_col_title4   varchar2(30);
  v_col_flag4    number;
  v_col_snap_id5 number;
  v_col_title5   varchar2(30);
  v_col_flag5    number;
  v_col_snap_id6 number;
  v_col_title6   varchar2(30);
  v_col_flag6    number;
  v_col_snap_id7 number;
  v_col_title7   varchar2(30);
  v_col_flag7    number;
  v_sql_len      number default 14;
  v_remark       varchar2(100);
  v_p_schema     varchar2(100);
  v_first_load   varchar2(38);

  v_col_num1  number;
  v_col_exec1 number;
  v_col_num2  number;
  v_col_num3  number;
  v_col_num4  number;
  v_col_num5  number;
  v_col_num6  number;
  v_col_num7  number;

  v_col_show1  varchar2(30);
  v_col_eshow1 varchar2(30);
  v_col_show2  varchar2(30);
  v_col_show3  varchar2(30);
  v_col_show4  varchar2(30);
  v_col_show5  varchar2(30);
  v_col_show6  varchar2(30);
  v_col_show7  varchar2(30);

  v_count     number;
  v_max_exec  number;
  v_show_exec number;
  v_sql_used  number;
  v_show_per  varchar2(10);
  v_now_per   varchar2(10);
  v_sql_text  varchar2(30000);
  v_sql_rule  varchar2(100) default 'ALTER|UPDATE|INSERT|DELETE|SELECT';
  v_sql_type  varchar2(20);

begin

  v_col_flag1 := 0;
  v_col_flag2 := 0;
  v_col_flag3 := 0;
  v_col_flag4 := 0;
  v_col_flag5 := 0;
  v_col_flag6 := 0;
  v_col_flag7 := 0;

  v_per_len := 7;
  v_n       := 80;
  v_output1 := '  Top SQLStat Checking Starting  ';
  v_length  := trunc((v_n - length(v_output1)) / 2);
  v_flag1   := lpad('*', v_length, '*');

  dbms_output.put_line(v_flag1 || v_output1 || v_flag1);
  dbms_output.put_line(' ');

  delete from snap_show_config where id = 3;
  delete from snap_show where snap_type_id = 3;

  for cur_inst in (select host_name,
                          inst_id,
                          instance_name,
                          version,
                          startup_time
                     from gv$instance) loop

    dbms_output.put_line('Instance >>( ' || cur_inst.inst_id ||
                         ' )<< Hostname: ' || cur_inst.host_name ||
                         ' Startup: ' ||
                         to_char(cur_inst.startup_time, 'yyyymmdd hh24:mi') ||
                         ' Version: ' || cur_inst.version);

    for cur_snap_id in (select snap_id, end_interval_time, rownum row_num
                          from (select snap_id, end_interval_time
                                  from dba_hist_snapshot
                                 where end_interval_time >
                                       sysdate - v_snap_ago
                                   and instance_number = cur_inst.inst_id
                                 order by snap_id desc)) loop
      if cur_snap_id.row_num <= 4 then
        if cur_snap_id.row_num = 1 then
          v_col_snap_id1 := cur_snap_id.snap_id;
          v_col_title1   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 2 then
          v_col_snap_id2 := cur_snap_id.snap_id;
          v_col_title2   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 3 then
          v_col_snap_id3 := cur_snap_id.snap_id;
          v_col_title3   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        elsif cur_snap_id.row_num = 4 then
          v_col_snap_id4 := cur_snap_id.snap_id;
          v_col_title4   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
        end if;
      else
        if cur_snap_id.end_interval_time < sysdate - 3 / 48 and
           v_col_flag5 = 0 then
          v_col_snap_id5 := cur_snap_id.snap_id;
          v_col_title5   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag5    := 1;
        elsif cur_snap_id.end_interval_time < sysdate - 1 and
              v_col_flag6 = 0 then
          v_col_snap_id6 := cur_snap_id.snap_id;
          v_col_title6   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag6    := 1;
        elsif cur_snap_id.end_interval_time < sysdate - v_snap_ago + 1 and
              v_col_flag7 = 0 then
          v_col_snap_id7 := cur_snap_id.snap_id;
          v_col_title7   := to_char(cur_snap_id.end_interval_time,
                                    'mmdd hh24:mi');
          v_col_flag7    := 1;
        end if;
      end if;
    end loop;

    if cur_inst.inst_id = 1 then

      v_output1 := '  Top SQLStat - Physical Read Bytes ';
      v_length  := trunc((v_n - length(v_output1)) / 2);
      v_flag1   := lpad('*', v_length, '*');

      dbms_output.put_line(v_flag1 || v_output1 || v_flag1);
      dbms_output.put_line(' ');
    end if;

    select sum(physical_read_bytes_delta)
      into v_max_exec
      from dba_hist_sqlstat a
     where a.snap_id = v_col_snap_id1
       and a.instance_number = cur_inst.inst_id;

    select sum(physical_read_bytes_delta)
      into v_show_exec
      from (select physical_read_bytes_delta
              from dba_hist_sqlstat a
             where a.snap_id = v_col_snap_id1
               and a.instance_number = cur_inst.inst_id
             order by a.physical_read_bytes_delta desc)
     where rownum <= v_exec_rownum;

    v_show_per := round(v_show_exec / v_max_exec * 100, 2) || '%';

    procas_719_standard_row_output(null,
                                   10,
                                   v_sql_len + v_per_len * 2 || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_titel_len || ',' ||
                                   v_titel_len || ',' || v_type_len || ',' ||
                                   v_remark_len,
                                   ',',
                                   '(' || v_show_per || ')Sql Id' || ',' ||
                                   v_col_title1 || ',' || v_col_title2 || ',' ||
                                   v_col_title3 || ',' || v_col_title4 || ',' ||
                                   v_col_title5 || ',' || v_col_title6 || ',' ||
                                   v_col_title7 || ',' || 'SqlType' || ',' ||
                                   'Remark');
    insert into snap_show_config
      (id,
       col1,
       col2,
       col3,
       col4,
       col5,
       col6,
       col7,
       col8,
       col9,
       col10,
       col11,
       col12,
       show_type,
       show_title,
       inst_info)
    values
      (3,
       v_show_per,
       'Sql Id',
       'SQL Exec count',
       v_col_title1,
       v_col_title2,
       v_col_title3,
       v_col_title4,
       v_col_title5,
       v_col_title6,
       v_col_title7,
       'SqlType',
       'Remark',
       'TOL SQL',
       v_output1,
       'Instance >>( ' || cur_inst.inst_id || ' )<< Hostname: ' ||
       cur_inst.host_name || ' Startup: ' ||
       to_char(cur_inst.startup_time, 'yyyymmdd hh24:mi') || ' Version: ' ||
       cur_inst.version);

    for cur_exec in (select sql_id
                       from (select sql_id
                               from dba_hist_sqlstat a
                              where a.snap_id = v_col_snap_id1
                                and a.instance_number = cur_inst.inst_id
                              order by a.physical_read_bytes_delta desc)
                      where rownum <= v_exec_rownum) loop

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id1
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select sum(physical_read_bytes_delta),
               trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END)),
               (CASE
                 WHEN sum(executions_delta) = 0 THEN
                  1
                 else
                  sum(executions_delta)
               END)
          into v_sql_used, v_col_num1, v_col_exec1
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id1
           and instance_number = cur_inst.inst_id;
        v_col_show1  := funcas_format_num_output(v_col_num1, 'Bytes');
        v_col_eshow1 := funcas_format_num_output(v_col_exec1, 'Times');

        select count(*)
          into v_count
          from gv$sql
         where sql_id = cur_exec.sql_id
           and inst_id = cur_inst.inst_id;
        if v_count <> 0 then
          select min(parsing_schema_name), min(first_load_time)
            into v_p_schema, v_first_load
            from gv$sql
           where sql_id = cur_exec.sql_id
             and inst_id = cur_inst.inst_id;
          v_remark := v_p_schema || '-' ||
                      trunc(sysdate -
                            to_date(v_first_load, 'yyyy-mm-dd/hh24:mi:ss')) || 'D';
        else
          v_remark := 'UNKNOW';
        end if;

      else
        v_col_num1  := 0;
        v_col_exec1 := 0;
        v_col_show1 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id2
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num2
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id2
           and instance_number = cur_inst.inst_id;
        v_col_show2 := funcas_format_num_output(v_col_num2, 'Bytes');
      else
        v_col_num2  := 0;
        v_col_show2 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id3
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num3
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id3
           and instance_number = cur_inst.inst_id;
        v_col_show3 := funcas_format_num_output(v_col_num3, 'Bytes');
      else
        v_col_num3  := 0;
        v_col_show3 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id4
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num4
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id4
           and instance_number = cur_inst.inst_id;
        v_col_show4 := funcas_format_num_output(v_col_num4, 'Bytes');
      else
        v_col_num4  := 0;
        v_col_show4 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id5
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num5
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id5
           and instance_number = cur_inst.inst_id;
        v_col_show5 := funcas_format_num_output(v_col_num5, 'Bytes');
      else
        v_col_num5  := 0;
        v_col_show5 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id6
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num6
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id6
           and instance_number = cur_inst.inst_id;
        v_col_show6 := funcas_format_num_output(v_col_num6, 'Bytes');
      else
        v_col_num6  := 0;
        v_col_show6 := 0;
      end if;

      select count(*)
        into v_count
        from dba_hist_sqlstat
       where sql_id = cur_exec.sql_id
         and snap_id = v_col_snap_id7
         and instance_number = cur_inst.inst_id;
      if v_count <> 0 then
        select trunc(sum(physical_read_bytes_delta) /
                     (CASE
                        WHEN sum(executions_delta) = 0 THEN
                         1
                        else
                         sum(executions_delta)
                      END))
          into v_col_num7
          from dba_hist_sqlstat
         where sql_id = cur_exec.sql_id
           and snap_id = v_col_snap_id7
           and instance_number = cur_inst.inst_id;
        v_col_show7 := funcas_format_num_output(v_col_num7, 'Bytes');
      else
        v_col_num7  := 0;
        v_col_show7 := 0;
      end if;

      v_now_per := round(v_sql_used / v_max_exec * 100, 2) || '%';

      select count(*)
        into v_count
        from dba_hist_sqltext
       where sql_id = cur_exec.sql_id;
      if v_count <> 0 then
        select regexp_substr(upper(sql_text), v_sql_rule, 1, 1)
          into v_sql_text
          from dba_hist_sqltext
         where sql_id = cur_exec.sql_id;
        if v_sql_text is null then
          v_sql_text := 'UNKNOW';
        end if;
      else
        v_sql_text := 'UNKNOW';
      end if;

      procas_719_standard_row_output(null,
                                     10,
                                     v_sql_len + v_per_len * 2 || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_titel_len || ',' ||
                                     v_titel_len || ',' || v_type_len || ',' ||
                                     v_remark_len,
                                     ',',
                                     '(' || v_now_per || ')' ||
                                     cur_exec.sql_id || '(' || v_col_eshow1 || ')' || ',' ||
                                     v_col_show1 || ',' || v_col_show2 || ',' ||
                                     v_col_show3 || ',' || v_col_show4 || ',' ||
                                     v_col_show5 || ',' || v_col_show6 || ',' ||
                                     v_col_show7 || ',' || v_sql_text || ',' ||
                                     v_remark);
          insert into snap_show
        (id,
         rate,
         sql_id,
         sql_exec_cnt,
         val1,
         val2,
         val3,
         val4,
         val5,
         val6,
         val7,
         val8,
         val9,
         snap_type_id)
      values
        (v_snap_show_id,
         v_now_per,
         cur_exec.sql_id,
         v_col_eshow1,
         v_col_show1,
         v_col_show2,
         v_col_show3,
         v_col_show4,
         v_col_show5,
         v_col_show6,
         v_col_show7,
         v_sql_text,
         v_remark,
         3);
      v_snap_show_id := v_snap_show_id + 1;

    end loop;

  /*
  v_output1:='  Top SQLStat - Cpu Used  ';
  v_length:=trunc((v_n-length(v_output1))/2);
  v_flag1:=lpad('*',v_length,'*');

  dbms_output.put_line(v_flag1||v_output1||v_flag1);
  dbms_output.put_line(' ');


  v_output1:='  Top SQLStat - Elapsed Time  ';
  v_length:=trunc((v_n-length(v_output1))/2);
  v_flag1:=lpad('*',v_length,'*');

  dbms_output.put_line(v_flag1||v_output1||v_flag1);
  dbms_output.put_line(' ');


  v_output1:='  Top SQLStat - Logic Read  ';
  v_length:=trunc((v_n-length(v_output1))/2);
  v_flag1:=lpad('*',v_length,'*');

  dbms_output.put_line(v_flag1||v_output1||v_flag1);
  dbms_output.put_line(' ');


  v_output1:='  Top SQLStat - Physical Read Bytes ';
  v_length:=trunc((v_n-length(v_output1))/2);
  v_flag1:=lpad('*',v_length,'*');

  dbms_output.put_line(v_flag1||v_output1||v_flag1);
  dbms_output.put_line(' ');
  */

  end loop;

  v_output1 := '  End Top SQLStat Check  ';
  v_length  := trunc((v_n - length(v_output1)) / 2);
  v_flag1   := lpad('*', v_length, '*');
  v_flag2   := lpad('*', v_n - v_length - length(v_output1), '*');

  dbms_output.put_line(v_flag1 || v_output1 || v_flag2);
  dbms_output.put_line(' ');

end;
/


prompt Done
spool off
set define on
