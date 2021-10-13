data = [time aG Fs no  Pt  Ieff  Tout Irradi T_amb Tin MTout Flow];
% 1. Hour
% 2. Collector aperture
% 3. Shadow Factor
% 4. Mean Efficiency
% 5. Tube percent
% 6. Effective Irradiance 
% 7. Real oulet Temperature
% 8. Irradiance W/m2
% 9. Ambiente Temperature
% 10. Inlet Temperature
% 11. Model Outlet Temperature
% 12. Flow m3/h


% Training data
T1=load('F060709.m');
T2=load('F100709.m');
T3=load('F160609.m');
T4=load('F220809.m'); 

% Checking data
C1=load('F290609.m');    
C2=load('F170809.m'); 

% Validation data
V1=load('datos15092011.m');    
V2=load('datos16092011.m'); 
V3=load('datos17092011.m');    
V4=load('DATA05102011.m'); 
V5=load('DATA110921.m'); 