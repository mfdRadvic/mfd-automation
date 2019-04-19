'''This module contains code running the MFD simplified battle simulator.'''
import pandas as pd
import numpy as np
import random

def main(side1='AlliedNations', side2='Akatsuki'):
    '''This runs the main function including loading the data, running
    combat and printing the data'''
    s1_df, s2_df = load_sides(side1=side1, side2=side2)
    ps1 = s1_df.copy()
    ps2 = s2_df.copy()
    while len(s1_df) > 0 and len(s2_df) > 0:
        combat_loop(s1_df, s2_df, side1, side2)
    save_results(s1_df, s2_df, side1=side1, side2=side2)

def load_sides(side1, side2):
    '''This loads the two sides of the conflict'''
    s1 = pd.read_csv(side1+'.csv')
    s2 = pd.read_csv(side2+'.csv')
    return s1, s2

def save_results(ps1, ps2, side1, side2):
    '''This saves the results of the conflict'''
    if len(ps1) > 0:
        print('{} has perished. Victory goes to {}.'.format(side2, side1))
    if len(ps2) > 0:
        print('{} has perished. Victory goes to {}.'.format(side1, side2))
    side1 = side1+'Post.csv'
    side2 = side2+'Post.csv'
    ps1.to_csv(side1,index=False)
    ps2.to_csv(side2,index=False)


def combat_loop(s1_df, s2_df, side1, side2):
    '''This runs the main combat loop'''
    s1_pow = calc_power(s1_df)
    print('{} rolled {}'.format(side1, s1_pow))
    s2_pow = calc_power(s2_df)
    print('{} rolled {}'.format(side2, s2_pow))
    wounds = calc_wounds(s1_pow, s2_pow, s1_df, s2_df)
    if wounds < 0: #Side 2 won
        print('{} won, distributing {} wounds'.format(side2, -wounds))
        distribute_wounds(-wounds, s1_df)
    else: #Side 1 won
        print('{} won, distributing {} wounds'.format(side1, wounds))
        distribute_wounds(wounds, s2_df)

def calc_wounds(pow1, pow2, s1_df, s2_df):
    '''This calculates how many wounds to give out'''
    wounds = (pow1 - pow2) / (pow1 + pow2)
    if wounds > 0:
        ava_wounds = len(s1_df)*2
        wounds = np.ceil(wounds* ava_wounds)
    else:
        ava_wounds = len(s2_df)*2
        wounds= np.floor(wounds * ava_wounds)
    print('Of {} potential wounds, {} were made'.format(ava_wounds, wounds))
    return wounds

def distribute_wounds(wounds, df):
    '''This distributes wounds to the losing side'''
    while wounds > 0 and len(df) > 0:
        injur_idx = random.randint(0,len(df)-1)
        df.loc[injur_idx,'Wounds'] += 1
        print('{} recieved a wound. Current Wounds = {}, max wounds = {}'.format(df.loc[injur_idx,'Name'],df.loc[injur_idx,'Wounds'],df.loc[injur_idx,'DefensiveBuffs']+2))
        if df.loc[injur_idx,'Wounds'] > (df.loc[injur_idx,'DefensiveBuffs'] + 1):
            print('{} has died. Removing from battle calculations'.format(df.loc[injur_idx,'Name']))
            df.drop(injur_idx,inplace=True)
            df.reset_index(inplace=True)
            df.drop('index',axis=1,inplace=True)
        wounds += -1

def calc_power(i_df, srank_wgt=0.1):
    '''This calculates the rolled power for a side'''
    df = i_df.copy() #copy dataframe to avoid unwanted edits
    df['FocusAdd'] = df['Focus'].apply(lambda x: 0.2 if x == 'Combat' else 0 if x is np.nan else -0.2)
    df['InjuryLimit'] = (df['DefensiveBuffs'] - df['Wounds'] + 2) / 2
    df['ones'] = 1
    df['InjuryMult'] = df.apply(lambda x: min(x['InjuryLimit'],1), axis=1)
    df['Multipler'] = (1 + df['S-ranks'] * srank_wgt + df['AlliedBuff'] + df['FocusAdd']) * df['InjuryMult']
    df['MaxPower'] = df['XP'] * df['Multipler']

    df['Power'] = df['MaxPower'] * np.random.rand(len(df))
    df['MaxWounds'] = df['DefensiveBuffs'] + 2
    print('Side Summary:')
    print(df[['Name','Power','MaxPower','MaxWounds','Wounds']])
    return df['Power'].sum()

if __name__ == '__main__':
    main()
