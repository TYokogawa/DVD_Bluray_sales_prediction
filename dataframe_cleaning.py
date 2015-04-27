__author__ = 'Tohei'

import pandas
import time


def time2digits(dataframe):
    year_row = []
    month_row = []
    date_row = []
    dtg_row = []
    widest_row = []
    runtime_row = []
    df = dataframe[dataframe.domestic_total_gross.notnull()]
    df = df[df.widest_release.notnull()]
    df = df[df.runtime.notnull()]
    df = df[df.runtime != 'N/A']
    df = df[df.release_date.notnull()]
    df = df[df.release_date != 'TBD']
    df = df[df.release_date != 'Winter 2015']
    df = df[df.release_date != '2011']
    df = df[df.release_date != 'N/A']
    df = df.dropna()

    ind = range(len(df.index))
    df.index = ind
    numrow = len(df.index)


    for i in range(numrow):
        try:
            data = df.ix[i,7]
            gross = df.ix[i,1]
            widest = df.ix[i,2]
            runtime = df.ix[i,6]

            time_digits = time.strptime(data, "%B %d, %Y")
            year_row.append(int(time_digits[0]))         ## year
            month_row.append(int(time_digits[1]))         ## month
            date_row.append(int(time_digits[2]))         ## date
            do_t_gross = gross.replace((','), '').replace(('$'), '').replace((' (Estimate)'),'')
            dtg_row.append(int(do_t_gross))
            wide_theat = widest.replace((' theaters'), '').replace((','), '')
            widest_row.append(int(wide_theat))
            run_min = hour2min(runtime)
            runtime_row.append(int(run_min))

        except:
            break

    df.insert(7, 'year', year_row)
    df.insert(8, 'month', month_row)
    df.insert(9, 'date', date_row)
    df.insert(1, 'domes_total_gross', dtg_row)
    df.insert(2, 'widest_theat', widest_row)
    df.insert(6, 'runtime_min', runtime_row)
    df = df.drop('domestic_total_gross', 1)
    df = df.drop('widest_release', 1)
    df = df.drop('runtime', 1)

    return df


def hour2min(timestring):
    min = timestring.replace((' hrs.'), '').replace((' min.'), '')
    h_min= min.split()
    total_min = int(h_min[0])*60 + int(h_min[1])
    return total_min


def weekdf2phi(weekly_dict):
    all_weekly_phi = pandas.DataFrame()
    weekly_df = pandas.DataFrame(weekly_dict.items(), columns=['title', ['weekly_gross', 'theaters']])
    weekly_df = weekly_df.replace(",", "")

    for mnum in range(len(weekly_df)):
        mv_week_df = pandas.DataFrame()
        titleinfo = weekly_df.iloc[mnum,:][0]
        wk_single =  weekly_df.iloc[mnum,:][1]
        numrow = wk_single.shape[0]

        for i in range(numrow):
            week = int(i+1)
            try:
                weekgross = wk_single.iloc[i,0]
                weektheat = wk_single.iloc[i,1]

                wk_gross = weekgross.replace(',', '').replace('$', '')

                try:
                    wk_gross = int(wk_gross)
                except:
                    None
                try:
                    wk_theat = weektheat.replace(' theaters', '').replace(',', '')

                except:
                    wk_theat = None
                try:
                    wk_theat = int(wk_theat)

                except:
                    None

                try:
                    per_theat = float(wk_gross)/wk_theat

                except:
                    per_theat = None

                if i == 0:
                    delta1_ptheat= 100
                else:
                    try:
                        try:
                            first_wk = int(mv_week_df.iloc[0,4])
                        except:
                            first_wk = 0
                        delta1_ptheat = float(per_theat)*100/ first_wk
                    except:
                        delta1_ptheat = 0
                if i == 0:
                    delta12_ptheat= 100
                elif i == 1:
                    delta12_ptheat=100
                else:
                    try:
                        try:
                            first_wk = int(mv_week_df.iloc[0,4])
                        except:
                            first_wk = 0
                        try:
                            second_wk = int(mv_week_df.iloc[1,4])
                        except:
                            second_wk = 0
                        if first_wk == 0:
                            first_wk = second_wk
                            delta12_ptheat = float(per_theat)*2*100 / (first_wk + second_wk)
                        elif second_wk == 0:
                            second_wk = 0
                            delta12_ptheat = float(per_theat)*2*100 / (first_wk + second_wk)
                        else:
                            delta12_ptheat = float(per_theat)*2*100 / (first_wk + second_wk)  ## used initial 2week gross average
                    except:
                        delta12_ptheat = 0

                aweek_df_t = pandas.DataFrame([week, titleinfo, wk_gross, wk_theat, per_theat, delta1_ptheat, delta12_ptheat, numrow], index=[0,1,2,3,4,5,6,7])

                aweek_df = aweek_df_t.T

                mv_week_df= mv_week_df.append(aweek_df, ignore_index=True)


            except:
                pass
        mv_week_df.columns = ['week','title','wk_gross','theater','wk_per_theat','delta1_per_theat', 'delta2wk_per_theat','rel_wk_max']
        all_weekly_phi = all_weekly_phi.append(mv_week_df)
    return all_weekly_phi


def rm_dollar(df):
    dtg_row = []
    widest_row = []
    ind = range(len(df.index))
    df.index = ind
    numrow = len(df.index)

    for i in range(numrow):
        try:
            gross = df.ix[i,1]
            widest = df.ix[i,2]
            do_t_gross = gross.replace(',', '').replace('$', '')
            dtg_row.append(int(do_t_gross))
            wide_theat = widest.replace(' theaters', '').replace(',', '')
            dtg_row.append(int(wide_theat))

        except:
            pass
    df.insert(1, 'domes_total_gross', dtg_row)
    df.insert(2, 'widest_theat', widest_row)

    df = df.drop('domestic_total_gross', 1)
    df = df.drop('widest_release', 1)

    return df


