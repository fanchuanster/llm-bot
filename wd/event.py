import pandas as pd
import os, sys

def set_pd_display_options(pd):
    pd.set_option("display.float_format", '{:.2f}'.format)
    pd.set_option("display.expand_frame_repr", False)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)     # optional
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

class Event:
    def __init__(self, event_csv_path):
        set_pd_display_options(pd)
        self.df = pd.read_csv(event_csv_path, dtype=str, names=["LogName", "col1","left","right","addr","how","col6","col7","col8","col9",
                                                                "col10", "col11","col12","col13","col14","col15","col16","col17"])
        self.df = self.df.iloc[:, :7]
        self.df = self.df.query("(LogName == 'Die Info') | ((LogName == 'UserLog') & (col6 == 'MBB'))")
        self.df[["left","right"]] = self.df[["left","right"]].astype('int32')
        # print(self.df.head())
        # print(len(self.df.index))
        # print(self.df.columns)

    def get_dict(self):
        df_die_info = self.df.query("LogName == 'Die Info'")
        key_columns = ['left', 'right']
        value_columns = ['addr']
        result_dict = df_die_info.set_index(key_columns)[value_columns].to_dict(orient='index')
        result_dict = {k:list(v.values())[0] for k,v in result_dict.items()}
        return result_dict
    
    def get_user_logs(self):
        user_logs = self.df.query("(LogName == 'UserLog') & (col6 == 'MBB')")
        user_logs = user_logs.drop_duplicates()
        user_logs = user_logs[['left', 'right','addr','how']]
        user_logs[['addr','how']] = user_logs[['addr','how']].astype('int32')
        valid_user_logs = user_logs.query("how != 0")
        return valid_user_logs
    
    def calc(self):
        user_logs = self.get_user_logs()
        # apply the core algorithm
        user_logs['o0'] = user_logs.apply(lambda row: row[2]*2 if row[3] & 1 else -1, axis=1)
        user_logs['o1'] = user_logs.apply(lambda row: row[2]*2 + 1 if row[3] & 2 else -1, axis=1)
        res = {}
        for key, sub_df in user_logs.groupby(['left', 'right']):
            res[key] = [[v for v in sub_df['o0'].tolist() if v!=-1], 
                        [v for v in sub_df['o1'].tolist() if v!=-1]]
        dict = self.get_dict()
        res0 = {(dict[k],*k,0):v[0] for k,v in res.items()}
        res1 = {(dict[k],*k,1):v[1] for k,v in res.items()}
        res0.update(res1)
        # dict to array
        res = [[*k, " ".join([str(hex(d)).replace("0x","") for d in v])] for k,v in res0.items()]
        return [r for r in res if r[4]]

if __name__ == "__main__":
    event_csv_path = sys.argv[1]
    event = Event(event_csv_path)
    # dict = event.get_dict()
    # print("dict:\n",dict)
    # user_logs = event.get_user_logs()
    output = event.calc()
    # print("output:",output)
    # print("calc output len:\n",len(output))
    o_df = pd.DataFrame(output, columns=["UID", "Channel", "Die", "Plan", "Result"])
    base_path, ext = os.path.splitext(event_csv_path)

    output_file_path = f"{base_path}_result{ext}"
    o_df.to_csv(output_file_path, index=False)
    print(f"result saved to {output_file_path}")
