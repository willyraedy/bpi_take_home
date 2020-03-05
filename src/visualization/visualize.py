import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

debates = [
  '2/19/2020',
  '2/7/2020',
  '1/14/2020',
  '12/19/2019',
  '11/20/2019',
  '10/15/2019',
  '09/12/2019'
]

primaries = ['2/29/2020', '2/22/2020', '2/11/2020', '2/3/2020']

def plot_lanes(df, progressives, moderates, race='National', show_range=False):
    plt.figure(figsize=(30,15))

    prog_data = df[(df.state == race) & (df.candidate_name.isin(progressives))]
    prog_grp = prog_data.groupby('modeldate').agg('sum')
    plt.plot(prog_grp.index, prog_grp.pct_estimate, label='Progressives')

    mod_data = df[(df.state == race) & (df.candidate_name.isin(moderates))]
    mod_grp = mod_data.groupby('modeldate').agg('sum')
    plt.plot(mod_grp.index, mod_grp.pct_estimate, label='Moderates')

    all_cand_natl = df[(df.state == race)]
    all_grp = all_cand_natl.groupby('modeldate').agg('sum')
    undecideds = 100 - all_grp.pct_estimate
    plt.plot(all_grp.index, undecideds, label='Undecideds')

    for d in debates:
      plt.axvline(pd.to_datetime(d), ls='--')
    for p in primaries:
      plt.axvline(pd.to_datetime(p), ls=':', c='red')
    plt.axvline(pd.to_datetime('11/24/2019'), c='black')

    if show_range:
      print('prog', np.min(prog_grp.pct_estimate), np.max(prog_grp.pct_estimate))
      print('mod', np.min(mod_grp.pct_estimate[:-5]), np.max(mod_grp.pct_estimate))
      print('und', np.min(undecideds[:-5]), np.max(undecideds[:-5]))
      plt.axhline(np.max(prog_grp.pct_estimate), c='b')
      plt.axhline(np.min(prog_grp.pct_estimate), c='b')
      plt.axhline(np.max(mod_grp.pct_estimate), c='orange')
      plt.axhline(np.min(mod_grp.pct_estimate[:-5]), c='orange')
      plt.axhline(np.max(undecideds[:-5]), c='green')
      plt.axhline(np.min(undecideds[:-10]), c='green')

    plt.title(f'{race} Polling By Lane', fontsize=30)
    plt.ylabel('Support (%)', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Date', fontsize=20)

    plt.legend(fontsize=20, loc='upper left')

def plot_candidates(df, candidates, race='National'):
  plt.figure(figsize=(30,15))
  for name in [x for x in df.candidate_name.unique() if x in candidates]:
      cand_data = df[(df.state == race) & (df.candidate_name == name)]
      plt.plot(cand_data.modeldate, cand_data.pct_estimate, label=name)
  for d in debates:
      plt.axvline(pd.to_datetime(d), ls='--')
  for p in primaries:
    plt.axvline(pd.to_datetime(p), ls=':', c='red')
  plt.axvline(pd.to_datetime('11/24/2019'), c='black')

  plt.title(f'{race} Polling By Candidate', fontsize=30)
  plt.ylabel('Support (%)', fontsize=20)
  plt.xticks(fontsize=20)
  plt.yticks(fontsize=20)
  plt.xlabel('Date', fontsize=20)
  plt.legend(fontsize=20, loc='upper left')
