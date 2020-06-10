import os
import psycopg2
import Tables.CreateAggregateTests as agt
import Tables.CreateMainTables as mt
import Tables.CreateOrganismResistance as ogr
import Config.Config as config

#createMain creates table w/ sampid, organism, unique values
def createMain():
    cur = config.conn.cursor()
    cmd = mt.MainTable
    cur.execute(cmd)
    cmInsert = mt.InsertData
    cur.execute(cmInsert)
    config.conn.commit()

#createMainAggregate creates table w/ sampid, organism for every match (duplicate sampids)
#This table may be dropped as it's not essential
def createMainAggregate():
    cur = config.conn.cursor()
    cmd = mt.MainTableAgg
    cur.execute(cmd)
    cmInsert = mt.InsertMainTableAll
    cur.execute(cmInsert)
    config.conn.commit()

#createMainNulls creates table w/ sampid, organism (with null organisms)
#This would be the table full of sampids that didn't match anything in
#the phenotype data set
def createMainNull():
    cur = config.conn.cursor()
    cmd = mt.MainTableNulls
    cur.execute(cmd)
    cmInsert = mt.InsertMainTableNulls
    cur.execute(cmInsert)
    config.conn.commit()

#createAggregate creates table w/ sampid matched with every test
#its corresponding hid/isolate aligns with
def createAggregate():
    cur = config.conn.cursor()
    cmd = agt.CreateTable
    cur.execute(cmd)
    cmInsert = agt.InsertData
    cur.execute(cmInsert)
    config.conn.commit()

#createResistance creates table w/ organisms and the tests/results
#that have been run against them.
def createResistance():
    cur = config.conn.cursor()
    cmd = ogr.CreateTable
    cur.execute(cmd)
    cmInsert = ogr.InsertData
    cur.execute(cmInsert)
    config.conn.commit()

#tableHandler generates SQL tables if enabled
#Tables can be found in the tables folder
def tableHandler(mode):
    print("Generating SQL tables...")
    if (mode == 1):
        createMain()
        #createMainAggregate needs to be built before
        #MainNull because it builds off it
        createMainAggregate()
        createMainNull()
        createAggregate()
        createResistance()
        print("Done generating SQL tables")
    else: 
        msg = "The mode is set to {}".format(mode)
        print (msg)
        