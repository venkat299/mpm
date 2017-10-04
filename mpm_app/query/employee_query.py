ADDITION = '''SELECT 1 as e_eis,'join' as category,ac_name AS reason,
            ac_value as cat_id,
                        a.*
                        FROM mpm_app_additioncat
                            LEFT JOIN
                                (
                            SELECT a_reason_id,
                      sum(CASE WHEN a_date BETWEEN '{curr_yr}-04-01' AND '{next_yr}-03-31' THEN 1 ELSE 0 END) AS curr_yr,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-04' THEN 1 ELSE 0 END) AS apr,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-05' THEN 1 ELSE 0 END) AS may,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-06' THEN 1 ELSE 0 END) AS jun,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-07' THEN 1 ELSE 0 END) AS jul,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-08' THEN 1 ELSE 0 END) AS aug,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-09' THEN 1 ELSE 0 END) AS sep,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-10' THEN 1 ELSE 0 END) AS oct,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-11' THEN 1 ELSE 0 END) AS nov,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{curr_yr}-12' THEN 1 ELSE 0 END) AS dec,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{next_yr}-01' THEN 1 ELSE 0 END) AS jan,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{next_yr}-02' THEN 1 ELSE 0 END) AS feb,
                      sum(CASE WHEN strftime('%Y-%m', a_date) = '{next_yr}-03' THEN 1 ELSE 0 END) AS mar,
                      sum(CASE WHEN a_date BETWEEN '{prev_yr}-04-01' AND '{curr_yr}-03-31' THEN 1 ELSE 0 END) AS prev_yr
                 FROM mpm_app_addition
                 WHERE mpm_app_addition.a_unit_id LIKE '%{filter}%'
                GROUP BY a_reason_id
                    )
                        a ON a.a_reason_id = mpm_app_additioncat.ac_value
    union
    
    SELECT 1 AS e_eis,
           'join' AS category,
           'Transfer_In' AS reason,
           'Transfer_In' AS cat_id,
           a.*
    from (SELECT 'Transfer_In' as t_reason_id,
                      sum(CASE WHEN th_date BETWEEN '{curr_yr}-04-01' AND '{next_yr}-03-31' THEN 1 ELSE 0 END) AS curr_yr,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-04' THEN 1 ELSE 0 END) AS apr,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-05' THEN 1 ELSE 0 END) AS may,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-06' THEN 1 ELSE 0 END) AS jun,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-07' THEN 1 ELSE 0 END) AS jul,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-08' THEN 1 ELSE 0 END) AS aug,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-09' THEN 1 ELSE 0 END) AS sep,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-10' THEN 1 ELSE 0 END) AS oct,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-11' THEN 1 ELSE 0 END) AS nov,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-12' THEN 1 ELSE 0 END) AS dec,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{next_yr}-01' THEN 1 ELSE 0 END) AS jan,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{next_yr}-02' THEN 1 ELSE 0 END) AS feb,
                      sum(CASE WHEN strftime('%Y-%m', th_date) = '{next_yr}-03' THEN 1 ELSE 0 END) AS mar,
                      sum(CASE WHEN th_date BETWEEN '{prev_yr}-04-01' AND '{curr_yr}-03-31' THEN 1 ELSE 0 END) AS prev_yr
                 FROM (
                          SELECT mpm_app_transferhistory.*
                          FROM mpm_app_transferhistory
                          WHERE 
                          mpm_app_transferhistory.th_unit_id LIKE '%{filter}%' 
                         and  mpm_app_transferhistory.th_prev_unit_id not LIKE '%{filter}%' 
                      )
        
       ) a
    '''

REDUCTION = '''
    SELECT 1 as e_eis,'term' as category,tc_name AS reason,
                tc_value as cat_id,
                            a.*
                            FROM mpm_app_TerminationCat
                                LEFT JOIN
                                    (
                                SELECT t_reason_id,
                          sum(CASE WHEN t_date BETWEEN '{curr_yr}-04-01' AND '{next_yr}-03-31' THEN 1 ELSE 0 END) AS curr_yr,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-04' THEN 1 ELSE 0 END) AS apr,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-05' THEN 1 ELSE 0 END) AS may,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-06' THEN 1 ELSE 0 END) AS jun,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-07' THEN 1 ELSE 0 END) AS jul,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-08' THEN 1 ELSE 0 END) AS aug,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-09' THEN 1 ELSE 0 END) AS sep,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-10' THEN 1 ELSE 0 END) AS oct,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-11' THEN 1 ELSE 0 END) AS nov,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{curr_yr}-12' THEN 1 ELSE 0 END) AS dec,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{next_yr}-01' THEN 1 ELSE 0 END) AS jan,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{next_yr}-02' THEN 1 ELSE 0 END) AS feb,
                          sum(CASE WHEN strftime('%Y-%m', t_date) = '{next_yr}-03' THEN 1 ELSE 0 END) AS mar,
                          sum(CASE WHEN t_date BETWEEN '{prev_yr}-04-01' AND '{curr_yr}-03-31' THEN 1 ELSE 0 END) AS prev_yr
                    FROM mpm_app_Termination
                    WHERE mpm_app_Termination.t_unit_id LIKE '%{filter}%'
                    GROUP BY t_reason_id
                        )
                    a ON a.t_reason_id = mpm_app_TerminationCat.tc_value
        union

        SELECT 1 AS e_eis,
               'term' AS category,
               'Transfer_Out' AS reason,
               'Transfer_Out' AS cat_id,
               a.*
        from (SELECT 'Transfer_Out' as t_reason_id,
                          sum(CASE WHEN th_date BETWEEN '{curr_yr}-04-01' AND '{next_yr}-03-31' THEN 1 ELSE 0 END) AS curr_yr,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-04' THEN 1 ELSE 0 END) AS apr,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-05' THEN 1 ELSE 0 END) AS may,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-06' THEN 1 ELSE 0 END) AS jun,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-07' THEN 1 ELSE 0 END) AS jul,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-08' THEN 1 ELSE 0 END) AS aug,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-09' THEN 1 ELSE 0 END) AS sep,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-10' THEN 1 ELSE 0 END) AS oct,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-11' THEN 1 ELSE 0 END) AS nov,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{curr_yr}-12' THEN 1 ELSE 0 END) AS dec,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{next_yr}-01' THEN 1 ELSE 0 END) AS jan,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{next_yr}-02' THEN 1 ELSE 0 END) AS feb,
                          sum(CASE WHEN strftime('%Y-%m', th_date) = '{next_yr}-03' THEN 1 ELSE 0 END) AS mar,
                          sum(CASE WHEN th_date BETWEEN '{prev_yr}-04-01' AND '{curr_yr}-03-31' THEN 1 ELSE 0 END) AS prev_yr
                     FROM (
                          SELECT mpm_app_transferhistory.*
                          FROM mpm_app_transferhistory
                          WHERE mpm_app_transferhistory.th_prev_unit_id LIKE '%{filter}%' 

                         and  mpm_app_transferhistory.th_unit_id not  LIKE '%{filter}%' 
                          )
            
           ) a
    '''