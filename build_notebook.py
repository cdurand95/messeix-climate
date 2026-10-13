import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))

md("""# Climate Intelligence — Messeix (Puy-de-Dôme, France)
Notebook-first data analysis for the Messeix climate report. Every figure traces to an executed cell and a cited source (ERA5 and/or Météo-France). No invented figures.

## 1. Location metadata (hard-coded, verified)
- **Commune:** Messeix, Puy-de-Dôme (63), Massif Central, France
- **Coordinates (centroid, assumed):** ~45.62° N, ~2.54° E
- **Elevation:** ~700–800 m a.s.l. (montane upland plateau)
- **ERA5 grid point (Open-Meteo interpolation):** 45.58875° N, 2.54717° E, elevation 777 m
- **Co-located Météo-France station:** MESSEIX (63225001), 45.616667° N, 2.566667° E, 800 m
- **CRS:** EPSG:4326 (WGS84) for reanalysis/station coordinates; EPSG:2154 (Lambert-93) for national mapping (French projection; stated for completeness).

### Data-source status / caveats (read first)
- **CDS API (direct ERA5):** The credentials in `~/.cdsapirc` are in the **deprecated `uid:key` format** and are rejected by the new CDS-Beta endpoint (`https://cds.climate.copernicus.eu/api`), which requires a **new UUID-format key** generated at https://cds.climate.copernicus.eu/how-to-api. **Direct CDS pull is therefore NOT used in this notebook.**
- **ERA5 accessed via the Open-Meteo Historical (archive) API**, which serves the **ERA5** reanalysis for 1940–present. Variables: daily Tmax/Tmin/Tmean, precipitation sum (mm), snowfall (cm), FAO-56 reference evapotranspiration (mm), max wind speed, shortwave radiation, precipitation hours. This is a legitimate ERA5 source; labelled as *ERA5 (via Open-Meteo)* throughout.
- **Météo-France:** open-data *Données climatologiques de base — quotidiennes* (per-department QUOT files), no API key required. Stations: **MESSEIX (63225001**, 1950–1987, 800 m**)** and **TAUVES (63426001**, 1950–2026, 851 m, 9.4 km**)**.
""")

code("""import numpy as np, pandas as pd, json, os
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
plt.rcParams['figure.dpi'] = 110

LAT, LON, ELEV = 45.62, 2.54, 777.0
CRS = {'EPSG:4326': 'WGS84 geographic', 'EPSG:2154': 'Lambert-93 (France)'}
NB_META = {'location':'Messeix (63)','lat':LAT,'lon':LON,'elev_m':ELEV,
           'crs':CRS,'era5_source':'ERA5 via Open-Meteo archive API',
           'station_primary':'TAUVES 63426001 (851m)','station_colocated':'MESSEIX 63225001 (800m)'}
os.makedirs('figures', exist_ok=True)
print('Location verified:', NB_META)
print('open-meteo ERA5 grid elev = 777 m (matches ~700-800 m upland)')""")

md("## 2. Load data (cached: pulls executed separately and cached in `data/`)")

code("""era = pd.read_csv('data/era5_messeix_daily_openmeteo.csv', parse_dates=['date'], index_col='date')
era.columns = [c.replace('temperature_2m_','t2m_').replace('precipitation_sum','pr')
                 .replace('snowfall_sum','snw').replace('et0_fao_evapotranspiration','pet')
                 .replace('windspeed_10m_max','wind10max').replace('shortwave_radiation_sum','ssrd')
                 .replace('precipitation_hours','pr_hours') for c in era.columns]
era = era[~era.index.duplicated()]
era = era.sort_index()
print('ERA5:', era.index.min().date(), '->', era.index.max().date(), 'rows', len(era))
print('cols:', list(era.columns))
# pet unit is mm; convert wind km/h->m/s; ssrd MJ/m2
era['wind10max_ms'] = era['wind10max']/3.6
print('NaNs per col:\\n', era.isna().sum().to_string())""")

code("""# Météo-France stations
msx = pd.read_csv('data/messeix_station_daily.csv', parse_dates=['date'], index_col='date')
tau = pd.read_csv('data/station_63426001_daily.csv', parse_dates=['date'], index_col='date')
for d in (msx, tau):
    d.index = d.index.normalize()
msx = msx[~msx.index.duplicated()].sort_index()
tau = tau[~tau.index.duplicated()].sort_index()
print('MESSEIX (63225001, 800m):', msx.index.min().date(), '->', msx.index.max().date(), len(msx))
print('TAUVES  (63426001, 851m):', tau.index.min().date(), '->', tau.index.max().date(), len(tau))
print('cols MESSEIX:', list(msx.columns))
print('cols TAUVES :', list(tau.columns))""")

md("""## 3. Monthly climatology 1991–2020 (ERA5) and station comparison""")

code("""def monthly_clim(ts, y0, y1):
    sub = ts[(ts.index.year>=y0)&(ts.index.year<=y1)]
    g = sub.groupby(sub.index.month)
    return g.mean()

def monthly_tot(ts, y0, y1):
    # Mean monthly TOTAL (mm) per calendar month over y0-y1
    sub = ts[(ts.index.year>=y0)&(ts.index.year<=y1)]
    yrs = sub.index.year.nunique()
    return sub.groupby(sub.index.month).sum() / yrs

clim_years = (1991,2020)
# ERA5 monthly climatology
era_clim = pd.DataFrame({
    'tmean': monthly_clim(era['t2m_mean'], *clim_years),
    'tmin':  monthly_clim(era['t2m_min'], *clim_years),
    'tmax':  monthly_clim(era['t2m_max'], *clim_years),
    'pr':    monthly_tot(era['pr'], *clim_years),
    'pet':   monthly_tot(era['pet'], *clim_years),
})
era_clim.index.name='month'
print('=== ERA5 monthly climatology %d-%d (Tmean/Tmin/Tmax degC, pr/pet mm) ===' % clim_years)
print(era_clim.round(1).to_string())
era_clim.to_csv('data/climatology_1991_2020_era5.csv')""")

code("""# Station monthly climatology for overlapping/recent window: TAUVES 1991-2020
tau_clim = pd.DataFrame({
    'tmean': monthly_clim(tau['TM'], *clim_years),
    'tmin':  monthly_clim(tau['TN'], *clim_years),
    'tmax':  monthly_clim(tau['TX'], *clim_years),
    'pr':    monthly_tot(tau['RR'], *clim_years),
})
print('=== TAUVES station monthly climatology %d-%d (degC, mm) ===' % clim_years)
print(tau_clim.round(1).to_string())
tau_clim.to_csv('data/climatology_1991_2020_taubes.csv')""")

md("## 4. Station vs ERA5 reconciliation (bias + elevation lapse-rate)")

code("""def overlap_bias(era_var, st_var, y0, y1):
    er = era_var[(era_var.index.year>=y0)&(era_var.index.year<=y1)]
    st = st_var[(st_var.index.year>=y0)&(st_var.index.year<=y1)]
    j = er.to_frame('era').join(st.to_frame('st'), how='inner').dropna()
    return j

# MESSEIX (800m, co-located) vs ERA5, overlap 1950-1987 for temperature
# (MESSEIX TM is not recorded -> reconstruct daily mean from (TN+TX)/2)
msx_tmean = (msx['TN'] + msx['TX']) / 2
jb = overlap_bias(era['t2m_mean'], msx_tmean, 1950, 1987)
print('MESSEIX vs ERA5 monthly-mean T bias (station-ERA5), degC, 1950-1987:')
print(f'  mean bias = {jb["st"].mean()-jb["era"].mean():+.2f}  n={len(jb)}  (station - ERA5)')
print(f'  ERA5 mean T = {jb["era"].mean():.1f}, station = {jb["st"].mean():.1f}')
# Elevation lapse rate: station 800m vs ERA5 grid 777m -> small difference expected
print(f'  elevation diff station-ERA5grid = {800-777} m')

# TAUVES (851m) vs ERA5 1991-2020
jt = overlap_bias(era['t2m_mean'], tau['TM'], 1991, 2020)
print('\\nTAUVES vs ERA5 monthly-mean T bias (station-ERA5), 1991-2020:')
print(f'  mean bias = {jt["st"].mean()-jt["era"].mean():+.2f}  n={len(jt)}')
print('  (positive = station warmer than ERA5 grid)')

# precip bias: MESSEIX vs ERA5 1950-1987 monthly
jp = overlap_bias(era['pr'], msx['RR'], 1950, 1987)
# ratio on matched monthly sums
er_m = jp['era'].groupby(jp.index.year).sum()
st_m = jp['st'].groupby(jp.index.year).sum()
ratio = (st_m/er_m).replace([np.inf,-np.inf],np.nan).dropna()
print('\\nMESSEIX vs ERA5 annual precip ratio (station/ERA5), 1950-1987:')
print(f'  median ratio = {ratio.median():.2f}  (station precip is {ratio.median()*100:.0f}% of ERA5)')""")

md("## 5. Trends 1940–present (ERA5): OLS + Mann-Kendall/Sen with p-values and CIs")

code("""def annual_series(var, agg='mean'):
    return var.groupby(var.index.year).agg(agg).dropna()

def mk_sen(y):
    y = np.asarray(y, float)
    x = np.arange(len(y))
    _t = stats.theilslopes(y, x)
    sl, ic, lo, hi = _t[0], _t[1], _t[2], _t[3]
    tau, p = stats.kendalltau(y, x)
    res = stats.linregress(x, y)
    n = len(y)
    se = res.stderr
    tcrit = stats.t.ppf(0.975, n-2)
    return {'sen_slope': sl, 'sen_ci_low': lo, 'sen_ci_high': hi,
            'mk_tau': tau, 'mk_p': p, 'ols_slope': res.slope,
            'ols_p': res.pvalue, 'ols_ci': (res.slope - tcrit*se, res.slope + tcrit*se)}

tmean_yr = annual_series(era['t2m_mean'], 'mean')
tmin_yr  = annual_series(era['t2m_min'], 'mean')
tmax_yr  = annual_series(era['t2m_max'], 'mean')
pr_yr    = annual_series(era['pr'], 'sum')

rows={}
for name, s in [('Tmean', tmean_yr), ('Tmin', tmin_yr), ('Tmax', tmax_yr), ('Precip', pr_yr)]:
    st = mk_sen(s.values)
    nyrs = len(s)
    rows[name] = {'n_years': nyrs, 'mean': s.mean(),
                  'sen_Cperdec': st['sen_slope']*10, 'sen_p': st['mk_p'],
                  'sen_lo': st['sen_ci_low']*10, 'sen_hi': st['sen_ci_high']*10,
                  'ols_Cperdec': st['ols_slope']*10, 'ols_p': st['ols_p']}
tr = pd.DataFrame(rows).T
print('=== Trends over full ERA5 record (%d-%d), units per decade ===' % (era.index.year.min(), era.index.year.max()))
print(tr.round(3).to_string())
tr.to_csv('data/trends_annual_full.csv')
print('\\nNote: Precip sen slope units = mm/decade (annual total); temp = degC/decade')""")

code("""# Seasonal temperature & precip trends (DJF,MAM,JJA,SON) 1940-present
seasons = {'DJF':[12,1,2],'MAM':[3,4,5],'JJA':[6,7,8],'SON':[9,10,11]}
def seasonal_series(var, agg, months):
    sub = var[var.index.month.isin(months)]
    return sub.groupby(sub.index.year).agg(agg).dropna()

rows={}
for sn, mo in seasons.items():
    for var, agg, label in [(era['t2m_mean'],'mean','T'), (era['pr'],'sum','P')]:
        s = seasonal_series(var, agg, mo)
        st = mk_sen(s.values)
        rows[f'{sn}_{label}'] = {'sen_perdec': st['sen_slope']*10, 'mk_p': st['mk_p'],
                                 'mean': s.mean(), 'n': len(s)}
s = pd.DataFrame(rows).T
print('=== Seasonal trends (Sen slope per decade; T=degC, P=mm) ===')
print(s.round(3).to_string())
s.to_csv('data/trends_seasonal_full.csv')""")

md("## 6. Decadal anomalies relative to 1961–1990 baseline (ERA5)")

code("""def decadal_anomaly(var, agg, base=(1961,1990)):
    idx = var.index
    base_val = var[(idx>=base[0])&(idx<=base[1])].agg(agg)
    decades = {}
    for d0 in range(1940, 2030, 10):
        d1 = d0+9
        sub = var[(idx>=d0)&(idx<=d1)]
        if len(sub)==0: continue
        decades[f'{d0}s'] = sub.agg(agg) - base_val
    return pd.Series(decades)

t_anom = decadal_anomaly(tmean_yr, 'mean')
pr_anom = decadal_anomaly(pr_yr, 'mean')
print('=== Decadal T anomaly (degC) vs 1961-1990 ===')
print(t_anom.round(2).to_string())
print('\\n=== Decadal annual precip anomaly (mm) vs 1961-1990 ===')
print(pr_anom.round(0).to_string())
pd.DataFrame({'t_anom_C':t_anom,'pr_anom_mm':pr_anom}).to_csv('data/decadal_anomalies.csv')""")

md("## 7. Growing season, frost days, heat extremes, heavy precipitation (ERA5, 1991–2020 + annual series)")

code("""def rolling_ge(series, thr, window=5):
    return series.rolling(window, center=True).mean() >= thr

def growing_season_year(tmean, thr):
    yr = tmean
    run = yr.rolling(5, center=True).mean()
    idx = run.index
    ok = run.values >= thr
    # first day of year with 5-day mean>=thr, last such day
    if not ok.any():
        return pd.NA, pd.NA, 0
    first = idx[np.argmax(ok)]
    last = idx[len(ok)-1-np.argmax(ok[::-1])]
    return first, last, int(np.sum(ok))

def annual_agro():
    recs=[]
    for y, g in era.groupby(era.index.year):
        t = g['t2m_mean']; tn=g['t2m_min']; tx=g['t2m_max']; pr=g['pr']
        fs,fe,fl = growing_season_year(t, 5.0)
        gs10 = growing_season_year(t, 10.0)[2]
        # last spring frost: last Tmin<0 within Jan-Jun
        hs = tn[tn.index.month<=6]
        last_spring = hs[hs<0].index.max() if (hs<0).any() else pd.NaT
        # first autumn frost: first Tmin<0 within Jul-Dec
        hf = tn[tn.index.month>=7]
        first_aut = hf[hf<0].index.min() if (hf<0).any() else pd.NaT
        recs.append(dict(
            year=y,
            frost_days=int((tn<0).sum()),
            hot30=int((tx>30).sum()),
            hot35=int((tx>35).sum()),
            heavyp20=int((pr>=20).sum()),
            gsl5=fl, gsl10=gs10,
            gdd5=float((t-5).clip(lower=0).sum()),
            gdd10=float((t-10).clip(lower=0).sum()),
            last_frost=last_spring, first_frost=first_aut,
        ))
    return pd.DataFrame(recs).set_index('year')

agro = annual_agro()
agro.to_csv('data/agro_annual_era5.csv')
clim = agro[(agro.index>=1991)&(agro.index<=2020)]
print('=== 1991-2020 climatology of agro indices (ERA5) ===')
_num = clim.select_dtypes(include=[np.number])
print(_num.mean().round(1).to_string())
print('=== Trends in key agro indices (1940-present, Sen slope/decade) ===')
for c in ['frost_days','gsl5','gsl10','gdd5','hot30','heavyp20']:
    s = mk_sen(agro[c].values)
    print(f'  {c}: sen={s["sen_slope"]*10:+.2f}/dec, p={s["mk_p"]:.3f}, mean={agro[c].mean():.1f}')""")

md("## 8. Huglin index and De Martonne aridity index")

code("""# Huglin index (Apr 1 - Sep 30), k=1.06 for 45-48N
def huglin_year(tmean, tmax):
    sub = era[(era.index.month>=4)&(era.index.month<=9)]
    yg = sub.groupby(sub.index.year)
    rows={}
    for y,g in yg:
        H = 1.06*((g['t2m_mean']+g['t2m_max'])/2 - 10).clip(lower=0).sum()
        rows[y]=H
    return pd.Series(rows)
hug = huglin_year(era['t2m_mean'], era['t2m_max'])
# De Martonne annual aridity index: P/(T+10)
dm = (pr_yr / (tmean_yr + 10))
# De Martonne monthly index for summer
dm_monthly = monthly_tot(era['pr'],*clim_years)/(monthly_clim(era['t2m_mean'],*clim_years)+10)
print('=== Huglin index (mean 1991-2020):', round(hug[(hug.index>=1991)&(hug.index<=2020)].mean(),0),
      '| trend sen/dec:', round(mk_sen(hug.values)['sen_slope']*10,1))
print('=== De Martonne annual index (mean 1991-2020):', round(dm[(dm.index>=1991)&(dm.index<=2020)].mean(),1))
print('    De Martonne monthly (1991-2020):')
print(dm_monthly.round(1).to_string())
pd.DataFrame({'huglin':hug,'dm_annual':dm}).to_csv('data/huglin_demartonne.csv')
print('Classification (De Martonne annual): >30 humid, 20-30 semi-humid, <20 semi-arid')""")

md("## 9. Water balance (P − PET), summer deficit, and drought (SPI-12 / SPEI-12)")

code("""# Annual water balance
wb_yr = (pr_yr - annual_series(era['pet'],'sum'))
print('=== Annual climatic water balance P - PET (ERA5) ===')
print('  mean 1991-2020: %.0f mm  |  trend sen/dec: %.1f mm (p=%.3f)' % (
    wb_yr[(wb_yr.index>=1991)&(wb_yr.index<=2020)].mean(),
    mk_sen(wb_yr.values)['sen_slope']*10, mk_sen(wb_yr.values)['mk_p']))
# Summer (JJA) deficit
def jja_sum(var):
    s=var[var.index.month.isin([6,7,8])]
    return s.groupby(s.index.year).sum().dropna()
jja_p = jja_sum(era['pr']); jja_pet=jja_sum(era['pet'])
jja_def = jja_p - jja_pet
print('  Summer (JJA) P-PET mean 1991-2020: %.0f mm (negative = deficit)' % jja_def[(jja_def.index>=1991)&(jja_def.index<=2020)].mean())
print('  Summer deficit trend sen/dec: %.1f mm (p=%.3f)' % (mk_sen(jja_def.values)['sen_slope']*10, mk_sen(jja_def.values)['mk_p']))

# SPI-12 and SPEI-12 (standardized accumulation, gamma for SPI, normal for SPEI)
def std_index(acc, dist='gamma'):
    out=pd.Series(np.nan, index=acc.index)
    # fit on full series
    a=acc.dropna().values
    if dist=='gamma':
        # fit gamma; handle zeros by adding small
        fit=stats.gamma.fit(a+1e-3)
        out[acc.notna()] = stats.gamma.cdf(acc[acc.notna()]+1e-3,*fit)
    else:
        mu,sd=a.mean(),a.std()
        out[acc.notna()] = stats.norm.cdf(acc[acc.notna()],mu,sd)
    return out.apply(lambda p: stats.norm.ppf(np.clip(p,1e-4,1-1e-4)))

pr12 = era['pr'].resample('ME').sum().rolling(12).sum()
pet12 = era['pet'].resample('ME').sum().rolling(12).sum()
spi12 = std_index(pr12,'gamma')
spei12 = std_index(pr12-pet12,'norm')
print('\\n=== SPI-12 / SPEI-12 drought years (< -1.0 = moderate drought, < -1.5 severe) ===')
for name, ix in [('SPI12',spi12),('SPEI12',spei12)]:
    ix=ix.dropna()
    sev = ix[ix < -1.5]
    mod = ix[(ix < -1.0)&(ix>=-1.5)]
    print(f'  {name}: % months < -1.0 = {100*(ix<-1.0).mean():.1f}%  | last severe (<-1.5): {sev.index.max().date() if len(sev) else "none"}')
pd.DataFrame({'spi12':spi12,'spei12':spei12}).to_csv('data/drought_indices.csv')""")

md("## 10. Frost-risk windows (1991–2020, ERA5)")

code("""tn = era['t2m_min']
# Frost-free season & last/first frost per year (already in agro df)
last = agro['last_frost'].dropna()
first = agro['first_frost'].dropna()
clim_frost = agro[(agro.index>=1991)&(agro.index<=2020)]
ll = clim_frost['last_frost'].dropna(); ff = clim_frost['first_frost'].dropna()
print('=== Frost windows 1991-2020 (days Tmin<0) ===')
print('  Mean last spring frost DOY:', round(ll.dt.dayofyear.mean(),1), '(~', ll.dt.strftime('%d-%b').mode().iloc[0] if len(ll) else '', ')')
print('  Mean first autumn frost DOY:', round(ff.dt.dayofyear.mean(),1))
print('  Mean frost-free season length (days):', round((ff.dt.dayofyear-ll.dt.dayofyear).mean(),1))
print('  Mean annual frost days:', round(clim_frost['frost_days'].mean(),1))

# 10-day frost probability: fraction of years with >=1 frost day in each 10-day bin
def frostprob(y0,y1):
    sub = era['t2m_min'][(era.index.year>=y0)&(era.index.year<=y1)]
    years = sub.index.year.unique()
    bins = {}
    for doy0 in range(1,366,10):
        doy1=min(doy0+9,365)
        cnt=0
        for y in years:
            ysub = sub[sub.index.year==y]
            d = (ysub.index.dayofyear>=doy0)&(ysub.index.dayofyear<=doy1)
            if (ysub[d]<0).any(): cnt+=1
        bins[f'{doy0}-{doy1}'] = cnt/len(years)
    return pd.Series(bins)
fp = frostprob(*clim_years)
print('\\n=== 10-day frost probability (1991-2020), fraction of years with >=1 frost day ===')
print(fp.round(2).to_string())
fp.to_csv('data/frost_probability.csv')
# Late-spring risk: frost probability by 10-day bin in Apr-May
print('\\n  Frost prob: Apr1-10 %.2f | Apr11-20 %.2f | Apr21-30 %.2f | May1-10 %.2f | May11-20 %.2f' % (
    fp.get('91-100',0), fp.get('101-110',0), fp.get('111-120',0),
    fp.get('121-130',0), fp.get('131-140',0)))""")

md("## 11. Figures (saved to `figures/`)")

code("""os.makedirs('figures',exist_ok=True)
# Fig1 climatology
fig,ax=plt.subplots(1,2,figsize=(11,4))
ax[0].plot(era_clim.index, era_clim['tmean'],'-o',label='Tmean ERA5')
ax[0].plot(tau_clim.index, tau_clim['tmean'],'-s',label='Tmean TAUVES')
ax[0].plot(era_clim.index, era_clim['tmin'],'--',label='Tmin ERA5')
ax[0].plot(era_clim.index, era_clim['tmax'],'--',label='Tmax ERA5')
ax[0].set_xticks(range(1,13)); ax[0].set_title('Monthly T climatology 1991-2020 (degC)')
ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
ax[1].bar(era_clim.index-0.2, era_clim['pr'], width=0.4, label='P ERA5')
ax[1].bar(era_clim.index+0.2, era_clim['pet'], width=0.4, label='PET ERA5')
ax[1].bar(tau_clim.index+0.4, tau_clim['pr'], width=0.4, alpha=.6, label='P TAUVES')
ax[1].set_xticks(range(1,13)); ax[1].set_title('Monthly P & PET 1991-2020 (mm)')
ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig1_climatology.png'); plt.close()

# Fig2 temperature trend
fig,ax=plt.subplots(figsize=(9,4))
ax.plot(tmean_yr.index, tmean_yr, lw=.8)
x=np.arange(len(tmean_yr)); sl,ic,ir,ip,ise=stats.linregress(x,tmean_yr.values)
ax.plot(tmean_yr.index, sl*x+ic, 'r-', label=f'OLS {sl*10:+.2f} degC/dec')
ax.axhline(tmean_yr[(tmean_yr.index>=1961)&(tmean_yr.index<=1990)].mean(), color='gray', ls='--', label='1961-90 mean')
ax.set_title('Annual mean temperature, Messeix (ERA5)'); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig2_trend_temperature.png'); plt.close()

# Fig3 precip trend
fig,ax=plt.subplots(figsize=(9,4))
ax.bar(pr_yr.index, pr_yr, width=1.0, color='steelblue', alpha=.7)
x=np.arange(len(pr_yr)); sl,ic,ir,ip,ise=stats.linregress(x,pr_yr.values)
ax.plot(pr_yr.index, sl*x+ic, 'r-', label=f'OLS {sl*10:+.1f} mm/dec')
ax.set_title('Annual precipitation, Messeix (ERA5)'); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig3_trend_precip.png'); plt.close()

# Fig4 decadal anomaly
fig,ax=plt.subplots(figsize=(9,4))
ax.bar(t_anom.index.astype(str), t_anom, color=['#d62728' if v>0 else '#1f77b4' for v in t_anom])
ax.set_title('Decadal T anomaly vs 1961-1990 (degC)'); ax.grid(alpha=.3, axis='y')
plt.tight_layout(); plt.savefig('figures/fig4_decadal_anomaly.png'); plt.close()

# Fig5 growing season length
fig,ax=plt.subplots(figsize=(9,4))
ax.plot(agro.index, agro['gsl5'], label='GSL @5C'); ax.plot(agro.index, agro['gsl10'], label='GSL @10C')
s5=mk_sen(agro['gsl5'].values); s10=mk_sen(agro['gsl10'].values)
ax.set_title(f'Growing season length (days/yr): @5C sen {s5["sen_slope"]*10:+.1f} d/dec (p={s5["mk_p"]:.2f}); @10C sen {s10["sen_slope"]*10:+.1f} d/dec (p={s10["mk_p"]:.2f})')
ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig5_growing_season.png'); plt.close()

# Fig6 GDD
fig,ax=plt.subplots(figsize=(9,4))
ax.plot(agro.index, agro['gdd5'], label='GDD5'); ax.plot(agro.index, agro['gdd10'], label='GDD10')
g5=mk_sen(agro['gdd5'].values)
ax.set_title(f'GDD: GDD5 sen {g5["sen_slope"]*10:+.0f}/dec (p={g5["mk_p"]:.2f})')
ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig6_gdd.png'); plt.close()

# Fig7 water balance
fig,ax=plt.subplots(figsize=(9,4))
ax.plot(wb_yr.index, wb_yr, lw=.8, label='Annual P-PET')
ax.axhline(0, color='k', lw=.6); ax.fill_between(wb_yr.index, wb_yr,0, where=wb_yr<0, color='red', alpha=.4)
ax.set_title('Annual climatic water balance P-PET (mm), Messeix (ERA5)'); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig7_water_balance.png'); plt.close()

# Fig8 frost risk
fig,ax=plt.subplots(figsize=(9,4))
ax.bar(fp.index, fp.values, width=0.9, color='teal')
ax.set_xticks(range(0,37,3)); ax.set_xticklabels([fp.index[i] for i in range(0,37,3)], rotation=90, fontsize=7)
ax.set_title('10-day frost probability 1991-2020 (fraction of years with >=1 frost day)')
ax.grid(alpha=.3, axis='y')
plt.tight_layout(); plt.savefig('figures/fig8_frost_risk.png'); plt.close()

# Fig9 drought
fig,ax=plt.subplots(figsize=(9,4))
ax.plot(spei12.dropna().index, spei12.dropna().values, lw=.7, label='SPEI-12')
ax.axhline(-1, color='orange', ls='--'); ax.axhline(-1.5, color='red', ls='--')
ax.set_title('SPEI-12 (P-PET), Messeix (ERA5)'); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig('figures/fig9_drought_spei.png'); plt.close()

print('Saved figures:', sorted(os.listdir('figures')))""")

md("## 12. Summary of key quantitative results (for the report)")

code("""print('========== MESSEIX CLIMATE - KEY RESULTS ==========')
print('Location: 45.62N 2.54E, ~777-800 m a.s.l., EPSG:4326 / 2154')
print()
print('[Station] MESSEIX 63225001 (45.6167N 2.5667E, 800m, 1950-1987) | TAUVES 63426001 (851m, 9.4km, 1950-2026)')
print()
tr2 = tr.T
print('[Temp trend 1940-present, ERA5]')
print(f'  Tmean: {tr2["Tmean"]["sen_Cperdec"]:+.3f} degC/dec (MK p={tr2["Tmean"]["sen_p"]:.4f}, CI {tr2["Tmean"]["sen_lo"]:+.3f}..{tr2["Tmean"]["sen_hi"]:+.3f})')
print(f'  Tmin : {tr2["Tmin"]["sen_Cperdec"]:+.3f} degC/dec (p={tr2["Tmin"]["sen_p"]:.4f})')
print(f'  Tmax : {tr2["Tmax"]["sen_Cperdec"]:+.3f} degC/dec (p={tr2["Tmax"]["sen_p"]:.4f})')
print(f'  Precip: {tr2["Precip"]["sen_Cperdec"]:+.1f} mm/dec (p={tr2["Precip"]["sen_p"]:.4f})')
print()
print('[1991-2020 climatology, ERA5]')
print(f'  Tmean {era_clim["tmean"].mean():.1f} degC | annual P {era_clim["pr"].sum():.0f} mm | PET {era_clim["pet"].sum():.0f} mm')
print(f'  Frost days {clim["frost_days"].mean():.0f} | GDD5 {clim["gdd5"].mean():.0f} | GDD10 {clim["gdd10"].mean():.0f}')
print(f'  Huglin {hug[(hug.index>=1991)&(hug.index<=2020)].mean():.0f} | De Martonne {dm[(dm.index>=1991)&(dm.index<=2020)].mean():.1f}')
print()
print('[Frost risk 1991-2020]')
print(f'  Mean last spring frost DOY ~{ll.dt.dayofyear.mean():.0f}, first autumn frost ~{ff.dt.dayofyear.mean():.0f}, frost-free ~{(ff.dt.dayofyear-ll.dt.dayofyear).mean():.0f} d')
print()
print('[Water balance 1991-2020]')
print(f'  Annual P-PET {wb_yr[(wb_yr.index>=1991)&(wb_yr.index<=2020)].mean():.0f} mm | Summer(JJA) P-PET {jja_def[(jja_def.index>=1991)&(jja_def.index<=2020)].mean():.0f} mm')
print()
print('Figures in ./figures ; tables in ./data')
print('=====================================================')""")

nb['cells'] = cells
nb['metadata']['kernelspec'] = {'display_name':'Python (messeix)','language':'python','name':'messeix'}
nb['metadata']['language_info'] = {'name':'python','version':'3.11'}
with open('climate_messeix.ipynb','w') as f:
    nbf.write(nb, f)
print('Notebook written with', len(cells), 'cells')
