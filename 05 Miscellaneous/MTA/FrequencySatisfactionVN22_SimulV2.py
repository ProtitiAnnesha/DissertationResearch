########################################
#
# @file Frequency.py
# @author: Annesha Enam, BUET
# @date: 20 March, 2014
#
#######################################

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

##
# Latent variable: income. Not directly observed. Respondents have
# only reported an income category, or have decided not to reveal it
#
###
#Structural model: we assume, for the sake of the example, that income
#is a function of age and gender.
###

b_meanSat = Beta('b_meanSat',8.59,-100,100,0 )
b_gender = Beta('b_gender',-0.122,-10000,10000,0 )
#b_age = Beta('b_age',0.00982,-10000,10000,0 )
#b_age1 = Beta('b_age1',0,-10000,10000,0 )
b_age2 = Beta('b_age2',-0.408,-10000,10000,0 )
b_age3 = Beta('b_age3',-0.272,-10000,10000,0 )
b_sigma = Beta('b_sigma',1.40,-10,10,0 )
#b_income = Beta('b_income',-0.000978,-10000,10000,0 )
#b_emailSubs = Beta('b_emailSubs',0,-10000,10000,0 )
#b_realTime = Beta('b_realTime',0.129,-10000,10000,0 )
#b_income2 = Beta('b_income2',0,-10000,10000,0 )
#b_income3 = Beta('b_income3',0,-10000,10000,0 )
#b_income4 = Beta('b_income4',0,-10000,10000,0 )
#b_income5 = Beta('b_income5',0,-10000,10000,0 )
b_commute = Beta('b_commute',-0.586,-10000,10000,0 )
#b_ridingLen = Beta('b_ridingLen',0,-10000,10000,0 )
#b_hisp = Beta('b_hisp',0,-10000,10000,0 )
b_black = Beta('b_black',-0.202,-10000,10000,0 )
#b_asian = Beta('b_asian',0,-10000,10000,0 )
#b_hhSize = Beta('b_hhSize',0,-10000,10000,0 )

#Error term of the structural model
omega = RandomVariable('omega')
density = bioNormalPdf(omega)

Freq = DefineVariable('Freq', ( Frequency <= 2 ) * 1 + ( ( Frequency > 2 ) & ( Frequency <= 4 ) ) * 2 + ( ( Frequency > 4 ) & ( Frequency <= 6 )  ) * 3 )
###Freq2 - does not include people who used it only for once, that is just for the first time#####################
Freq2 = DefineVariable('Freq2', ( Frequency <= 2 ) * 1 + ( ( Frequency > 2 ) & ( Frequency <= 4 ) ) * 2 + ( ( Frequency > 4 ) & ( Frequency <= 5 )  ) * 3 )
Age1 = DefineVariable('Age1', (Age == 1))#less than 18
Age2 = DefineVariable('Age2', (Age == 2) | (Age == 3))#18 to 34
Age3 = DefineVariable('Age3', (Age == 4) | (Age == 5))#35 to 54
Age4 = DefineVariable('Age4', (Age == 6) | (Age == 7)) #Age 55 and above
Age35Above = DefineVariable('Age35Above', (Age3 == 1) | (Age4 == 1))
maleDummy = DefineVariable('maleDummy', ( Gender == 1 ))
Income_rec = DefineVariable('Income_rec', ( Income == 1 ) * 12.5 + ( Income == 2 ) * 18.75 + (Income == 3) * 31.25 + (Income == 4) * 43.75 + (Income == 5) * 62.5 + (Income == 6) * 87.5 + (Income == 7) * 150 + (Income == 8) * 250 + (Income == 9 ) * 300)
Age_cont = DefineVariable('Age_cont', ( Age == 1 ) * 18 + ( Age == 2 ) * 21 + (Age == 3) * 29.5 + (Age == 4) * 39.5 + (Age == 5) * 49.5 + (Age == 6) * 59.5 + (Age == 7) * 65 )
Income1 = DefineVariable('Income1', (Income == 1) | (Income == 2))#Less than $25,000 yearly
Income2 = DefineVariable('Income2', (Income == 3) | (Income == 4))#Less than $50,000 yearly
Income3 = DefineVariable('Income3', (Income == 5) | (Income == 6))#Less than $100,000 yearly
Income4 = DefineVariable('Income4', (Income == 7) | (Income == 8))#Less than $200,000 yearly
Income5 = DefineVariable('Income5', (Income == 9))#More than $200,000 yearly
Commute = DefineVariable('Commute', (TripPurpose == 1) | (TripPurpose == 2) | (TripPurpose == 3) )
NonCommute = DefineVariable('NonCommute', (TripPurpose == 4) | (TripPurpose == 5) | (TripPurpose == 6) )
#zeroToThreeYears = DefineVariable('zeroToThreeYears', ( RidingMetroNorthLengthRec == 1 ) | ( RidingMetroNorthLengthRec == 2 ) )
#threeToTenYears = DefineVariable('threeToTenYears', ( RidingMetroNorthLengthRec == 3 ) | ( RidingMetroNorthLengthRec == 4 ) )
moreThanTen = DefineVariable('moreThanTen', ( RidingMetroNorthLengthRec == 5 ) )
EmailSub = DefineVariable('EmailSub', ( Q67 == 1 ) )
realTime = DefineVariable('realTime', ( Q70b == 1 ) )
hisp = DefineVariable('hisp', ( Q78 == 1 ) ) #Hispanic dummy
black = DefineVariable('black', ( Race == 2 ) ) #Black dummy
asian = DefineVariable('asian', ( Race == 4 ) ) # Asian dummy
hhSizeDum = DefineVariable('hhSizeDum', ( HHSize > 2 ) ) # HH size dummy - 1 if size greater than 4

# Satisfaction
satisfaction = b_meanSat + b_gender * maleDummy + b_age2 * Age2 + b_age3 * Age3 + b_commute * Commute + b_black * black + b_sigma * omega

#Parameters to be estimated
# Arguments:
#   - 1  Name for report; Typically, the same as the variable.
#   - 2  Starting value.
#   - 3  Lower bound.
#   - 4  Upper bound.
#   - 5  0: estimate the parameter, 1: keep it fixed.
#
ASC_daily = Beta('Daily const.',-0.791,-100,100,0)
ASC_weekly = Beta('Weekly const.',0.0503,-100,100,0)
ASC_monthly = Beta('Monthly const.',0,-10,10,1)
B_GenderDaily = Beta('Male Dummy Daily',0.191,-10,10,0)
#B_GenderWeekly = Beta('Male Dummy Weekly',0.0602,-10,10,0)
#B_Age2Daily = Beta('Age 18 to 34 Daily',0907,-10,10,0)
#B_Age3Daily = Beta('Age 35 to 54 Daily',1.52,-10,10,0)
B_Age35AbDaily = Beta('Age 35 to above Daily',0.763,-10,10,0)
#B_Age2Weekly = Beta('Age 18 to 34 Weekly',0.847,-10,10,0)
B_Age3Weekly = Beta('Age 35 to 54 Weekly',0.628,-10,10,0)
B_Age4Weekly = Beta('Age 55 to above Weekly',0.788,-10,10,0)
#B_incomeDaily = Beta('Income mid points Daily',0.00284,-10,10,0)
#B_incomeWeekly = Beta('Income mid points Weekly',0.00282,-10,10,0)
#B_income = Beta('Income mid points',0.00224,-10,10,0)
B_income2Dal = Beta('Income2Dal',0.555,-10,10,0)
B_income3Dal = Beta('Income3Dal',0.551,-10,10,0)
B_income4Dal = Beta('Income4Dal',0.563,-10,10,0)
B_income5Dal = Beta('Income5DAl',0.918,-10,10,0)
B_income2Wek = Beta('Income2Wek',-0.593,-10,10,0)
B_income3Wek = Beta('Income3Wek',-0.634,-10,10,0)
B_income4Wek = Beta('Income4Wek',-0.684,-10,10,0)
#B_income5Wek = Beta('Income5Wek',0,-10,10,0)
B_satDaily = Beta('satisfaction overall daily',-0.153,-10,10,0)
B_satWeekly = Beta('satisfaction overall weekly',0.0113,-10,10,0)
#B_satDailyRLen = Beta('satisfaction Rlength daily',-0.0736,-10,10,0)
#B_satWeeklyRLen = Beta('satisfaction Rlength weekly',-0.0662,-10,10,0)
#B_satDailyAge = Beta('satisfaction young daily',-0.144,-10,10,0)
#B_satWeeklyAge = Beta('satisfaction young weekly',-0.127,-10,10,0)
#B_satDailyInc = Beta('satisfaction poor daily',0,-10,10,0)
B_satWeeklyInc = Beta('satisfaction poor weekly',-0.0761,-10,10,0)
B_satComDaily = Beta('satisfaction Commute Daily',-0.196,-10,10,0)
B_satComWeekly = Beta('satisfaction Commute Weekly',-0.265,-10,10,0)
B_satHispDaily = Beta('satisfaction hispanic Daily',-0.361,-10,10,0)
#B_satHispWeekly = Beta('satisfaction hispanic Weekly',0.0,-10,10,0)
#B_satBlackDaily = Beta('satisfaction black Daily',-0.179,-10,10,0)
#B_satBlackWeekly = Beta('satisfaction black Weekly',-0.0440,-10,10,0)
B_satAsianDaily = Beta('satisfaction asian Daily',0.287,-10,10,0)
#B_satAsianWeekly = Beta('satisfaction asian Weekly',0.0,-10,10,0)
#B_satHHSizeDal = Beta('satisfaction hhSize Daily',-0.0354,-10,10,0)
B_satHHSizeWeek = Beta('satisfaction hhSize Weekly',0.192,-10,10,0)
B_comDal = Beta('Commute Daily',5.31,-10,10,0)
B_comWeek = Beta('Commute Weekly',3.98,-10,10,0)
B_SatRLenDal = Beta('Satisfaction Riding Length Daily',-0.0656,-10,10,0)
B_SatRLenWeek = Beta('Satisfaction Riding Length Weekly',-0.0604,-10,10,0)
B_hispDal = Beta('Hispanic Daily',3.33,-10,10,0)
#B_hispWeek = Beta('Hispanic Weekly',0.292,-10,10,0)
B_blackDal = Beta('Black Daily',0.539,-10,10,0)
#B_blackWeek = Beta('Black Weekly',0.973,-10,10,0)
B_asianDal = Beta('Asian Daily',-1.91,-10,10,0)
#B_asianWeek = Beta('Asian Weekly',0.321,-10,10,0)
#B_hhSizeDal = Beta('HH Size Daily',-0.193,-10,10,0)
B_hhSizeWeek = Beta('HH Size Weekly',-1.59,-10,10,0)


# Utility functions
# The following statements are designed to preprocess the data. It is
# like creating a new columns in the data file. This should be
# preferred to the statement like
# TRAIN_TT_SCALED = TRAIN_TT / 100.0
# which will cause the division to be reevaluated again and again,
# throuh the iterations. For models taking a long time to estimate, it
# may make a significant difference.
 
V1 = ASC_daily + B_Age35AbDaily * Age35Above + B_GenderDaily * maleDummy + B_income2Dal *  Income2 + B_income3Dal * Income3 + B_income4Dal * Income4 + B_income5Dal * Income5 + B_satDaily * satisfaction + B_comDal * Commute + B_hispDal * hisp + B_blackDal * black + B_asianDal * asian + B_satComDaily * (satisfaction * Commute) + B_satAsianDaily * (satisfaction * asian) + B_satHispDaily * (satisfaction * hisp) + B_SatRLenDal * (satisfaction * moreThanTen)
V2 = ASC_weekly + B_Age3Weekly * Age3 + B_Age4Weekly * Age4 + B_income2Wek *  Income2 + B_income3Wek * Income3 + B_income4Wek * Income4 + B_satWeekly * satisfaction + B_comWeek * Commute + B_hhSizeWeek * hhSizeDum  + B_satComWeekly * (satisfaction * Commute) + B_satHHSizeWeek * (satisfaction * hhSizeDum) + B_satWeeklyInc * (satisfaction * Income1) + B_SatRLenWeek * (satisfaction * moreThanTen)
V3 = ASC_monthly

# Associate utility functions with the numbering of alternatives
V = {1: V1,
     2: V2,
     3: V3}

# Associate the availability conditions with the alternatives
#CAR_AV_SP =  DefineVariable('CAR_AV_SP',CAR_AV  * (  SP   !=  0  ))
#TRAIN_AV_SP =  DefineVariable('TRAIN_AV_SP',TRAIN_AV  * (  SP   !=  0  ))

CondProb1 = exp(V1) / (exp(V1)+exp(V2)+exp(V3))
CondProb2 = exp(V2) / (exp(V1)+exp(V2)+exp(V3))
CondProb3 = exp(V3) / (exp(V1)+exp(V2)+exp(V3))

#Prob1 = exp(V1) / (exp(V1)+exp(V2)+exp(V3))
#Prob2 = exp(V2) / (exp(V1)+exp(V2)+exp(V3))
#Prob3 = exp(V3) / (exp(V1)+exp(V2)+exp(V3))

Prob1 = Integrate(CondProb1 * density, 'omega')
Prob2 = Integrate(CondProb2 * density, 'omega')
Prob3 = Integrate(CondProb3 * density, 'omega')

# Defines an itertor on the data
rowIterator('obsIter') 

exclude = (( Frequency == 999 ) + ( Frequency == 6 ) + (  Age   ==  999  ) + ( Gender == 999 ) + (Income == 999) + (TripPurpose == 999) + (Q2 == 999) + (Q1 == 999) + (Q50 == 999) + (Q3 == 999) + (Q13 == 999) + (Q21 == 999) + (Q28 == 999) + (Q32 == 999) + ( RidingMetroNorthLengthRec == 999 ) + (Q78 == 999) + (Race == 999) + (HHSize == 999) ) 

BIOGEME_OBJECT.EXCLUDE = exclude

simulate = {'Prob. Daily': Prob1,
			'Prob. Weekly': Prob2,
			'Prob. Monthly': Prob3 }



#DO NOT MODIFY THIS
BIOGEME_OBJECT.SIMULATE = Enumerate(simulate,'obsIter')
