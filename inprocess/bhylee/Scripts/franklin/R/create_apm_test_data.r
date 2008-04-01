# Contents of "c:\my.cnf":
# 
# [activity_pattern_model_test_data]
# user = urbansim
# password = UwmYsqlAt.5
# host = trondheim.cs.washington.edu
# dbname=activity_pattern_model_test_data
# database=activity_pattern_model_test_data

library(DBI)
library(RMySQL)

# set up connection
cnx_apm <- dbConnect(dbDriver("MySQL"), group="activity_pattern_model_test_data")

# zones
n.zones<-20
zones<-data.frame( cbind( total_area = exp(rnorm(n.zones, log(1000))),
                          logsum_multiplier = rep(0,n.zones),
                          area_type = round(runif(n.zones, min=-0.49999, max=4.49999)),
                          school_area = exp(rnorm(n.zones, log(50))),
                          high_school_enrollment = exp(rnorm(n.zones, log(500))),
                          ft_college_enrollment = exp(rnorm(n.zones, log(500))),
                          pt_college_enrollment = exp(rnorm(n.zones, log(200))),
                          cie_employment = exp(rnorm(n.zones, log(500))),
                          pdr_employment = exp(rnorm(n.zones, log(500))),
                          service_employment = exp(rnorm(n.zones, log(500))),
                          health_employment = exp(rnorm(n.zones, log(500))),
                          mips_employment = exp(rnorm(n.zones, log(500))),
                          retail_employment = exp(rnorm(n.zones, log(500))),
                          agricultural_employment = exp(rnorm(n.zones, log(500))),
                          manufacturing_employment = exp(rnorm(n.zones, log(500))),
                          trade_employment = exp(rnorm(n.zones, log(500))),
                          other_employment = exp(rnorm(n.zones, log(500))),
                          school_zone = round(runif(n.zones)),
                          college_zone = round(runif(n.zones)),
                          number_school_buildings = rpois(n.zones, lambda=1),
                          county_id = round(runif(n.zones, min=0.5, max=9.49999)),
                          pef_network_connectivity = round(runif(n.zones, min=0.5, max=3.49999)),
                          pef_vitality = round(runif(n.zones, min=0.5, max=3.49999)),
                          pef_topology = round(runif(n.zones, min=0.5, max=3.49999)),
                          pef_crossing = round(runif(n.zones, min=0.5, max=3.49999)),
                          pef_safety = round(runif(n.zones, min=0.5, max=3.49999))))
summary(zones)

dbSendQuery(cnx_apm, "delete from zones where 1=1")
dbWriteTable(cnx_apm, "zones", zones, append=T)

# travel_data

td.travel_data_id<-NULL
td.from_zone_id<-NULL
td.to_zone_id<-NULL
td.distance<-NULL
td.mode_choice_logsum<-NULL

for (z in 1:n.zones) {
    td.travel_data_id<-append(td.travel_data_id, 1:n.zones+(z-1)*n.zones)
    td.from_zone_id<-append(td.from_zone_id, rep(z, n.zones))
    td.to_zone_id<-append(td.to_zone_id, 1:n.zones)
    td.distance<-append(td.distance, rlnorm(n.zones))
    td.mode_choice_logsum<-append(td.mode_choice_logsum, rep(NA, n.zones))
}

travel_data<-data.frame( cbind(
    from_zone_id=td.from_zone_id,
    to_zone_id=td.to_zone_id,
    distance=td.distance,
    mode_choice_logsum=td.mode_choice_logsum))

travel_data[1:5,]
summary(travel_data)

dbSendQuery(cnx_apm, "delete from travel_data where 1=1")
dbWriteTable(cnx_apm, "travel_data", travel_data, append=T)

# travel_data_by_time_by_mode

n.times<-5
n.modes<-15

t.travel_data_by_time_by_mode_id<-NULL
t.travel_data_id<-NULL
t.from_zone_id<-NULL
t.to_zone_id<-NULL
t.time_period_id<-NULL
t.mode_id<-NULL
t.drive_time<-NULL
t.walk_time<-NULL
t.bike_time<-NULL
t.in_vehicle_time<-NULL
t.first_wait_time<-NULL
t.second_wait_time<-NULL
t.out_of_pocket_costs<-NULL
t.number_of_stops<-NULL
t.drive_access_time<-NULL

for (m in 1:n.modes) {
    for (tp in 1:n.times) {
        for (z in 1:n.zones) {
                t.travel_data_by_time_by_mode_id<-append(
                    t.travel_data_by_time_by_mode_id,
                    1:n.zones+(z-1)*n.zones+(tp-1)*n.zones*n.zones+(m-1)*n.zones*n.zones*n.times)
                t.travel_data_id<-append(
                    t.travel_data_id,
                    1:n.zones+(z-1)*n.zones)
                t.from_zone_id<-append(
                    t.from_zone_id,
                    rep(z,n.zones))
                t.to_zone_id<-append(
                    t.to_zone_id,
                    1:n.zones)
                t.time_period_id<-append(
                    t.time_period_id,
                    rep(tp,n.zones))
                t.mode_id<-append(
                    t.mode_id,
                    rep(m,n.zones))
                t.drive_time<-append(t.drive_time,exp(rnorm(n.zones, log(20))))
                t.walk_time<-append(t.walk_time,exp(rnorm(n.zones, log(100))))
                t.bike_time<-append(t.bike_time,exp(rnorm(n.zones, log(50))))
                t.in_vehicle_time<-append(t.in_vehicle_time,exp(rnorm(n.zones, log(40))))
                t.first_wait_time<-append(t.first_wait_time,exp(rnorm(n.zones, log(10))))
                t.second_wait_time<-append(t.second_wait_time,exp(rnorm(n.zones, log(5))))
                t.out_of_pocket_costs<-append(t.out_of_pocket_costs,exp(rnorm(n.zones, log(2.5))))
                t.number_of_stops<-append(t.number_of_stops,rpois(n.zones, lambda=1))
                t.drive_access_time<-append(t.drive_access_time,exp(rnorm(n.zones, log(10))))
        }
    }
}

# revise values for mode consistency:
t.drive_time[(t.mode_id== 2) | (t.mode_id== 3) | (t.mode_id== 4) | (t.mode_id== 5) |
             (t.mode_id==10) | (t.mode_id==11) | (t.mode_id==12) | (t.mode_id==13) |
             (t.mode_id==14) | (t.mode_id==15)]<-0
t.walk_time[(t.mode_id== 1) | (t.mode_id== 3) | (t.mode_id== 6) | (t.mode_id== 7) |
            (t.mode_id== 8) | (t.mode_id== 9) | (t.mode_id==14) | (t.mode_id==15)]<-0
t.bike_time[(t.mode_id!=3)]<-0
t.in_vehicle_time[(t.mode_id== 1) | (t.mode_id== 2) | (t.mode_id== 3) | (t.mode_id== 4) |
                  (t.mode_id== 7) | (t.mode_id== 8) | (t.mode_id== 9)]<-0
t.first_wait_time[(t.mode_id== 1) | (t.mode_id== 2) | (t.mode_id== 3) | (t.mode_id== 4) |
                  (t.mode_id== 7) | (t.mode_id== 8) | (t.mode_id== 9)]<-0
t.second_wait_time[(t.mode_id== 1) | (t.mode_id== 2) | (t.mode_id== 3) | (t.mode_id== 4) |
                   (t.mode_id== 7) | (t.mode_id== 8) | (t.mode_id== 9)]<-0
t.out_of_pocket_costs[(t.mode_id==2) | (t.mode_id==3)]<-0
t.number_of_stops[(t.mode_id== 1) | (t.mode_id== 2) | (t.mode_id== 3) | (t.mode_id== 4) |
                  (t.mode_id== 7) | (t.mode_id== 8) | (t.mode_id== 9)]<-0
t.drive_access_time[(t.mode_id<6) | ((t.mode_id>6) & (t.mode_id<14))]<-0


travel_data_by_time_by_mode<-data.frame( cbind( 
    travel_data_id=t.travel_data_id,
    from_zone_id=t.from_zone_id,
    to_zone_id=t.to_zone_id,
    time_period_id=t.time_period_id,
    mode_id=t.mode_id,
    drive_time=t.drive_time,
    walk_time=t.walk_time,
    bike_time=t.bike_time,
    in_vehicle_time=t.in_vehicle_time,
    first_wait_time=t.first_wait_time,
    second_wait_time=t.second_wait_time,
    out_of_pocket_costs=t.out_of_pocket_costs,
    number_of_stops=t.number_of_stops,
    drive_access_time=t.drive_access_time))

travel_data_by_time_by_mode[1:5,]
summary(travel_data_by_time_by_mode)

dbSendQuery(cnx_apm, "delete from travel_data_by_time_by_mode where 1=1")
dbWriteTable(cnx_apm, "travel_data_by_time_by_mode", travel_data_by_time_by_mode, append=T)

# households

n.hh<-100

h.household_id<-1:n.hh
h.zone_id<-round(runif(n.hh, min=0.5, max=n.zones+0.4999))
h.children<-rpois(n.hh, lambda=0.8)
h.adults<-1+rpois(n.hh, lambda=1)
h.income<-exp(rnorm(n.hh, log(25000)))
h.cars<-rpois(n.hh, lambda=1.7)
h.persons<-h.adults+h.children
h.workers<-round(runif(n.hh, min=0.33, max=h.adults+0.4999))
h.kids_under_5<-(runif(n.hh, min=0, max=18) < 5) & (h.children > 0)
h.couple_with_non_working_adult<-(h.adults>=2) & (h.workers<h.adults)

households<-data.frame( cbind(
    zone_id=h.zone_id,
    persons=h.persons,
    adults=h.adults,
    workers=h.workers,
    children=h.children,
    kids_under_5=h.kids_under_5,
    income=h.income,
    cars=h.cars,
    couple_with_non_working_adult=h.couple_with_non_working_adult))


households[1:5,]
summary(households)

dbSendQuery(cnx_apm, "delete from households where 1=1")
dbWriteTable(cnx_apm, "households", households, append=T)

# persons

p.person_id<-NULL
p.household_id<-NULL
p.actor_type<-NULL
p.employment<-NULL
p.licensed<-NULL
p.age<-NULL
p.sex<-NULL
p.job_id<-NULL

person_id<-0

agemean<-35
agesd<-0.55

for (h in 1:n.hh) {
    h.n.ad<-h.adults[h]
    h.n.ch<-h.children[h]
    workers.left<-h.workers[h]
    # adults:
    for (a in 1:h.n.ad) {
        person_id<-person_id+1
        p.person_id<-append(p.person_id, person_id)
        p.household_id<-append(p.household_id, h.household_id[h])
        if (workers.left>0) {
            p.employment<-append(p.employment, round(runif(1,min=1,max=2)))
            p.actor_type<-append(p.actor_type, 1)
            workers.left<-workers.left-1
        } else {
            p.employment<-append(p.employment, 0)
            p.actor_type<-append(p.actor_type, round(runif(1,min=2,max=3)))
        }
        p.licensed<-append(p.licensed, (runif(1)>0.1)*1)
        age<-0
        while ((age < 18) | (age > 100)) {
            age<-round(rlnorm(1, meanlog=log(agemean), sdlog=agesd))
        }
        p.age<-append(p.age, age)
        p.sex<-append(p.sex, round(runif(1))+1)
        p.job_id<-append(p.job_id, NA)
    }
    # children:
    if (h.n.ch > 0) {
        for (c in 1:h.n.ch) {
            person_id<-person_id+1
            p.person_id<-append(p.person_id, person_id)
            p.household_id<-append(p.household_id, h.household_id[h])
            if (workers.left>0) {
                p.employment<-append(p.employment, round(runif(1,min=1,max=2)))
                p.actor_type<-append(p.actor_type, 1)
                age<-0
                while ((age < 15) | (age > 17)) {
                    age<-round(rlnorm(1, meanlog=log(agemean), sdlog=agesd))
                }
                p.age<-append(p.age, age)
                workers.left<-workers.left-1
            } else {
                p.employment<-append(p.employment, 0)
                p.actor_type<-append(p.actor_type, 2)
                while ((age < 1) | (age > 17)) {
                    age<-round(rlnorm(1, meanlog=log(agemean), sdlog=agesd))
                }
                p.age<-append(p.age, age)            
            }
            if (age>16) {
                p.licensed<-append(p.licensed, round(runif(1, min=0.25, max=1)))
            } else {
                p.licensed<-append(p.licensed, 0)
            }
            p.sex<-append(p.sex, round(runif(1))+1)
            p.job_id<-append(p.job_id, NA)
        }
    }
}

persons<-data.frame( cbind(
    household_id=p.household_id,
    actor_type=p.actor_type,
    employment=p.employment,
    licensed=p.licensed,
    age=p.age,
    sex=p.sex,
    job_id=p.job_id))

persons[1:5,]
summary(persons)

dbSendQuery(cnx_apm, "delete from persons where 1=1")
dbWriteTable(cnx_apm, "persons", persons, append=T)


# specification & coefficients tables

# create them if not already there
dbSendQuery(cnx_apm, "create table workplace_location_choice_model_specification select * from Eugene_1980_baseyear_apm.employment_location_choice_model_specification")
dbSendQuery(cnx_apm, "create table workplace_location_choice_model_coefficients select * from Eugene_1980_baseyear_apm.employment_location_choice_model_coefficients")



dbSendQuery(cnx_apm, "delete from workplace_location_choice_model_specification where 1=1")
dbSendQuery(cnx_apm, "delete from workplace_location_choice_model_coefficients where 1=1")

