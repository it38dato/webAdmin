from django.shortcuts import render
from .models import Content
from rest_framework import viewsets
from .serializers import ContentSerializer
import pandas as pd
import mysql.connector
from mysql.connector import Error
from django.conf import settings
# Create your views here.
class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
def checkTable(check):
    return check.empty
def funcCorrectNumbBS(numb, numbFull):
    if len(numb) == 1:
        numbFull = "000" + numb
    elif len(numb) == 2:
        numbFull = "00" + numb
    elif len(numb) == 3:
        numbFull = "0" + numb
    elif len(numb) == 4:
        numbFull = numb
    else:
        print("- Enter the BS number correctly")
    return numb, numbFull
def funcCorrectRegBS(reg, numbReg, lnhoif, utc, msw, plan, arfcnMin, arfcnMax, eNodeB, satell, eArfcn):
    hostEricsson = settings.CONFIG_DATA.get("IPERICSSON")
    pathIpPlan = settings.CONFIG_DATA.get("PATHIPPLAN")
    if reg == "AN":
        numbReg = "87"
        lnhoif = ["1875", "3400", "", "", "", ""]
        utc = "UTC+12"
        msw = "МСК+9"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_AND"
        satell = "SATELL"
        eArfcn = "3400"
    elif reg == "BI":
        numbReg="79"
        lnhoif = ["1750", "1875", "1892", "6175", "6200", "3400"]
        utc = "UTC+10"
        msw = "МСК+7"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_BIR/"
        satell = "SATELL"
        eArfcn = "1750"
    elif reg == "HB":
        numbReg="27"
        lnhoif = ["1892", "6175", "6200", "3400", "50", "75"]
        utc = "UTC+10"
        msw = "МСК+7"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_HAB/"
        satell = "SATELL"
        eArfcn = "1892"
    elif reg == "KM":
        numbReg="41"
        lnhoif = ["1275", "1875", "3400", "6175", "75", ""]
        utc = "UTC+12"
        msw = "МСК+9"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_KAM/"
        satell = "SATELL"
        eArfcn = "1875"
    elif reg == "IR":
        numbReg="38"
        lnhoif = ["1875", "1425", "1400", "6175", "6200", "1250"]
        utc = "UTC+8"
        msw = "МСК+5"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_IRK/"
        satell = "SATELL"
        eArfcn = "1875"
    elif reg == "MD":
        numbReg="49"
        lnhoif = ["1875", "1425", "6175", "3400", "75", ""]
        utc = "UTC+11"
        msw = "МСК+8"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_MGD/"
        satell = "SATELL"
        eArfcn = "1425"
    elif reg == "SA":
        numbReg="65"
        lnhoif = ["1750", "6175", "6200", "3400", "75", "100"]
        utc = "UTC+11"
        msw = "МСК+8"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_SAH/"
        satell = "SATELL"
        eArfcn = "1750"
    elif reg == "YA":
        numbReg="14"
        lnhoif = ["1875", "6175", "3400", "", "", ""]
        utc = "UTC+9"
        msw = "МСК+6"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_YAK/"
        satell = "SATELL"
        eArfcn = "1875"
    elif reg == "IO":
        numbReg="88"
        lnhoif = ["1875", "", "", "", "", ""]
        utc = "UTC+8"
        msw = "МСК+5"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_IRK/"
        satell = "SATELL"
        eArfcn = "1875"
    elif reg == "AM":
        numbReg="28"
        lnhoif = ["125", "1875", "", "", "", "", "", "", "", "", "", ""]
        utc = "Etc/GMT-9"
        msw = "МСК+6"
        plan = pathIpPlan
        arfcnMin = 812
        arfcnMax = 885
        eNodeB = "eNodeB_BLG"
        eArfcn = ""
    elif reg == "BU":
        numbReg="3"
        lnhoif = ["1425", "1427", "1875", "1923", "3400", "6175", "6200", "38750", "38950", "39550", "39100", "39150"]
        utc = "Etc/GMT-8"
        msw = "МСК+5"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_BRT/"
        arfcnMin = 1
        arfcnMax = 100
        eNodeB = "eNodeB_BRT"
        eArfcn = ""
    elif reg == "VV":
        numbReg="25"
        lnhoif = ["100", "125", "1875", "3400", "6175", "6200", "38700", "38750", "38900", "38950", "", ""]
        utc = "Etc/GMT-10"
        msw = "МСК+7"
        plan = f"http://{hostEricsson}/CreateSite_web/CES/table_ip_plan_VLD/"
        arfcnMin = 812
        arfcnMax = 885
        eNodeB = "eNodeB_VLD"
        eArfcn = ""
    elif reg == "ZB":
        numbReg="75"
        lnhoif = ["1598", "1900", "75", "", "", "", "", "", "", "", "", ""]
        utc = "Etc/GMT-9"
        msw = "МСК+6"
        plan = pathIpPlan
        arfcnMin = 756
        arfcnMax = 772
        eNodeB = "eNodeB_CHI"
        eArfcn = ""
    else:
        print("- Enter region correctly")
        numbReg=""
        lnhoif = ["", "", "", "", "", ""]
        utc = ""
        msw = ""
        plan = "http://"
        satell = ""
        arfcnMin = 0
        arfcnMax = 0
        eNodeB = ""
        eArfcn = ""
    return reg, numbReg, lnhoif, utc, msw, plan, arfcnMin, arfcnMax, eNodeB, satell, eArfcn
def funcNokiaAddSublistSite(reg, numb, sublist):
    numbFull = ""
    numbReg = "" 
    timeUtc = ""
    timeMsw = ""
    ipPlan = ""
    subnetWork = ""
    listLnhoif = []
    arfcnMin = 0
    arfcnMax = 0
    satell = ""
    eArfcn = ""

    hostRdb = settings.CONFIG_DATA.get("HOSTRDB")    
    sublist.append(reg)
    sublist.append(numb)

    numb, numbFull = funcCorrectNumbBS(numb, numbFull)
    reg, numbReg, listLnhoif, timeUtc, timeMsw, ipPlan, arfcnMin, arfcnMax, subnetWork, satell, eArfcn = funcCorrectRegBS(reg, numbReg, listLnhoif, timeUtc, timeMsw, ipPlan, arfcnMin, arfcnMax, subnetWork, satell, eArfcn)

    sublist.append(numbFull)
    sublist.append(numbReg)
    sublist.append(numbReg+numbFull)
    sublist.append(reg+numbFull)
    sublist.append(reg+"00"+numbFull)
    sublist.append("https://"+hostRdb+"/p/list.aspx?op=list&k=c3a5t1r&v=c3a5ts5c1cs9r133&q="+reg+"00"+numbFull)

    sublist.append(str(int(numbFull)+3000))
    sublist.append(reg+str(int(numbFull)+3000))
    sublist.append(numbReg+str(int(numbFull)+3000))
    sublist.append(str(int(numbFull)+6000))    
    sublist.append(reg+str(int(numbFull)+6000))    
    sublist.append(numbReg+str(int(numbFull)+6000))

    if numbFull[0] == "0":
        sublist.append(str(int(numbFull)+4000))
        sublist.append(reg+str(int(numbFull)+4000))
        sublist.append(numbReg+str(int(numbFull)+4000))
    else:
        sublist.append(numbFull[:0]+"3"+numbFull[0+1:])
        sublist.append(reg+(numbFull[:0]+"3"+numbFull[0+1:]))
        sublist.append(numbReg+(numbFull[:0]+"3"+numbFull[0+1:]))

    for indexLnhoif in listLnhoif:
        sublist.append(indexLnhoif)

    sublist.append(timeUtc)
    sublist.append(timeMsw)
    sublist.append(ipPlan)
    
    sublist.append(satell)
    sublist.append(eArfcn)
    return reg, numb, sublist
def funcTestingOutList(listTest, index):
    print("======================TEST======================")
    count = 0
    for lists in listTest:
        count=count+1
        print(count," - ",lists)
    print("======================TEST======================")
    count = 0
    for listIndex in listTest[index]:
        for info in listIndex:
            print(str(count)," - ",info)
            count=count+1
    print("======================TEST======================")
    count = 0
    for listIndex in listTest[index]:
        count=count+1
        print(count, " - ", listIndex[0], " - ",listIndex)
    print("======================TEST======================")
    return listTest, index
def funcAddNumbers(listN, dfN):
    dfN = pd.DataFrame(listN)
    dfN.columns = ["Numbers"]
    return listN, dfN
def funcAddSublistFromTable(listFromTable, sublistFromTable, dfTable, lenObj, lenList, site):
    if checkTable(dfTable) == False:
        listTemp = dfTable.values.tolist()
        for indexLists in listTemp:
            for indexObject in indexLists:
                if ".0" in str(indexObject):
                    indexObject = str(int(indexObject))
                    sublistFromTable.append(indexObject)
                elif ("nan" in str(indexObject)) or ("NaN" in str(indexObject)):
                    indexObject = ""
                    sublistFromTable.append(str(indexObject))
                else:
                    sublistFromTable.append(str(indexObject))
    else:
        print("- There is no data "+site+" in the N_Data file from table (dfTable)")
        sublistTemp = []
        listTemp = []
        object = ""
        for indexLen in range(1,lenObj+1):
            sublistTemp.append(object)
        for indexLen in range(1, lenList+1):
            listTemp.append(sublistTemp)
        for indexLists in listTemp:
            for indexObject in indexLists:
                sublistFromTable.append(indexObject)
    listFromTable.append(sublistFromTable)
    return listFromTable, sublistFromTable, dfTable, lenObj, lenList, site
def funcAddListFromTable(mainList, subLsts, updateListTable, dfTable, lenObj, lenList, site):
    object = ""
    listTable = []
    if checkTable(dfTable) == False:
        listTable = dfTable.values.tolist()
        #print(listTable)
        for indexLists in listTable:
            #print(indexLists)
            updateIndexLists = []
            for indexObject in indexLists:
                #print(indexObject)
                #print(type(indexObject))
                if (".0" in str(indexObject)) and (".0." not in str(indexObject)) and (".0 " not in str(indexObject)):# добавил условие  ".0 ", 
                    #print(float(indexObject))
                    #print(int(float(indexObject)))
                    #print(str(int(float(indexObject))))
                    #indexObject = str(int(indexObject)) #Поменял так как 43.0 для мощности почему str не переводит на int, только через float
                    #indexLenObj = str(int(float(indexObject))) #Поменял так как не понятно почему indexLenObj а не indexObject
                    indexObject = str(int(float(indexObject)))
                elif ("nan" in str(indexObject)) or ("None" in str(indexObject)) or ("NaN" in str(indexObject)) or ("0x2a" in str(indexObject)):
                    indexObject = ""
                #print(indexObject)
                updateIndexLists.append(indexObject)
                subLsts.append(indexObject)#Убрал так как нету необходимости читать данные по каждому объекту
            #print(updateIndexLists)
            updateListTable.append(updateIndexLists)
        #print(subLsts)
        #print(updateListTable)
    else:
        print("- There is no data "+site+" in the table (dfTable)")
        for indexLenObj in range(0, lenObj):
            #print(indexLenObj)
            listTable.append(object)            
        print(listTable)
        for indexLenObj in range(1, lenList+1):
            #print(indexLenObj)
            updateListTable.append(listTable)
        print(updateListTable)        
        #for indexLists in updateListTable:
        #    for indexObject in indexLists:
        #        subLsts.append(indexObject)
        #print(subLsts)
    #mainList.append(subLsts)
    #mainList.append(updateListTable)
    #print(mainList)
    return mainList, subLsts, updateListTable, dfTable, lenObj, lenList, site
def funcMysqlPandas(fromExcel, df):
    conn = None
    listExcelLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU"]
    
    try:        
        # Установление соединения
        conn = mysql.connector.connect(
            host = settings.CONFIG_DATA.get("IPDBDJANGO"),
            user = settings.CONFIG_DATA.get("USERDBDJANGO"),
            passwd = settings.CONFIG_DATA.get("PASSWORDDBDJANGO"),
            database = settings.CONFIG_DATA.get("NAMEDBDJANGO")
        )
        if conn.is_connected():
            #print("Соединение с базой данных установлено успешно.")            
            # SQL-запрос, который мы хотим выполнить
            query = f"SELECT * FROM {fromExcel}"            
            # Использование pandas.read_sql_query для загрузки данных напрямую в DataFrame
            df = pd.read_sql_query(query, conn)
            df.columns = listExcelLetters[0:len(df.columns)]
            #print(f"\nДанные успешно загружены в DataFrame. Получено строк: {len(df)}")
    except Error as e:
        print(f"Ошибка при работе с MySQL: {e}")
    finally:
        # Закрытие соединения
        if conn is not None and conn.is_connected():
            conn.close()
            #print("Соединение с MySQL закрыто.")
    return fromExcel, df
def funcFilterTables24G3G(col, table, g42, g3):
    copyCol=table[col]
    table.insert(0, "Site", copyCol)
    table["Site"] = table["Site"].str[:6]
    dfTemp1 = table.loc[table["Site"] == g42]
    dfTemp2 = table.loc[table["Site"] == g3]
    table = pd.concat([dfTemp1, dfTemp2])
    return col, table, g42, g3
def funcNokiaStartList(reg, numb, listStart):
    listSite = []
    sublistSite = []
    listConnectionMap = []
    sublistConnectionMap = []
    listNumbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
    dfBscRncName = pd.DataFrame()

    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    listStart.append(listSite)

    dfSheet, dfCablink = funcMysqlPandas("nokia_cablink", pd.DataFrame())
    dfCablink0000 = dfCablink.loc[dfCablink["S"] == float(sublistSite[4])]    
    dfCablink3000 = dfCablink.loc[dfCablink["S"] == float(sublistSite[10])]    
    dfCablink6000 = dfCablink.loc[dfCablink["S"] == float(sublistSite[13])]    
    dfCablink4000 = dfCablink.loc[dfCablink["S"] == float(sublistSite[16])]
    dfCablink0000 = dfCablink0000.reindex(columns=["S", "T", "V", "W", "AC", "AB", "X", "Y"])
    dfCablink3000 = dfCablink3000.reindex(columns=["S", "T", "V", "W", "AC", "AB", "X", "Y"])
    dfCablink6000 = dfCablink6000.reindex(columns=["S", "T", "V", "W", "AC", "AB", "X", "Y"])
    dfCablink4000 = dfCablink4000.reindex(columns=["S", "T", "V", "W", "AC", "AB", "X", "Y"])
    listNumbers, dfNumbers = funcAddNumbers(listNumbers[0:26], pd.DataFrame())
    dfNumbers["Numbers"] = dfNumbers["Numbers"].astype("float64")
    dfCablink0000 = pd.merge(dfNumbers, dfCablink0000, left_on="Numbers", right_on="T", how="outer")
    dfCablink3000 = pd.merge(dfNumbers, dfCablink3000, left_on="Numbers", right_on="T", how="outer")
    dfCablink6000 = pd.merge(dfNumbers, dfCablink6000, left_on="Numbers", right_on="T", how="outer")
    dfCablink4000 = pd.merge(dfNumbers, dfCablink4000, left_on="Numbers", right_on="T", how="outer")
    dfConnectionMap=pd.merge(dfCablink0000, dfCablink3000, left_on="Numbers", right_on="Numbers", how="outer")
    dfConnectionMap=pd.merge(dfConnectionMap, dfCablink6000, left_on="Numbers", right_on="Numbers", how="outer")
    renameCol=dfConnectionMap["S_x"]
    dfConnectionMap.insert(0, "B18", renameCol)
    del dfConnectionMap["S_x"]   
    renameCol=dfConnectionMap["V_x"]
    dfConnectionMap.insert(1, "B", renameCol)
    del dfConnectionMap["V_x"]
    renameCol=dfConnectionMap["W_x"]
    dfConnectionMap.insert(2, "C", renameCol)
    del dfConnectionMap["W_x"]
    renameCol=dfConnectionMap["AC_x"]
    dfConnectionMap.insert(3, "D", renameCol)
    del dfConnectionMap["AC_x"]
    renameCol=dfConnectionMap["AB_x"]
    dfConnectionMap.insert(4, "E", renameCol)
    del dfConnectionMap["AB_x"]
    renameCol=dfConnectionMap["X_x"]
    dfConnectionMap.insert(5, "F", renameCol)
    del dfConnectionMap["X_x"]
    renameCol=dfConnectionMap["Y_x"]
    dfConnectionMap.insert(6, "G", renameCol)
    del dfConnectionMap["Y_x"]
    del dfConnectionMap["T_x"]
    renameCol=dfConnectionMap["S_y"]
    dfConnectionMap.insert(7, "H18", renameCol)
    del dfConnectionMap["S_y"]
    del dfConnectionMap["T_y"]
    renameCol=dfConnectionMap["V_y"]
    dfConnectionMap.insert(8, "H", renameCol)
    del dfConnectionMap["V_y"]
    renameCol=dfConnectionMap["W_y"]
    dfConnectionMap.insert(9, "I", renameCol)
    del dfConnectionMap["W_y"]
    renameCol=dfConnectionMap["AC_y"]
    dfConnectionMap.insert(10, "J", renameCol)
    del dfConnectionMap["AC_y"]
    renameCol=dfConnectionMap["AB_y"]
    dfConnectionMap.insert(11, "K", renameCol)
    del dfConnectionMap["AB_y"]
    renameCol=dfConnectionMap["X_y"]
    dfConnectionMap.insert(12, "L", renameCol)
    del dfConnectionMap["X_y"]
    renameCol=dfConnectionMap["Y_y"]
    dfConnectionMap.insert(13, "M", renameCol)
    del dfConnectionMap["Y_y"]
    renameCol=dfConnectionMap["S"]
    dfConnectionMap.insert(14, "N18", renameCol)
    del dfConnectionMap["S"]
    del dfConnectionMap["T"]
    renameCol=dfConnectionMap["V"]
    dfConnectionMap.insert(15, "N", renameCol)
    del dfConnectionMap["V"]
    renameCol=dfConnectionMap["W"]
    dfConnectionMap.insert(16, "O", renameCol)
    del dfConnectionMap["W"]
    renameCol=dfConnectionMap["AC"]
    dfConnectionMap.insert(17, "P", renameCol)
    del dfConnectionMap["AC"]
    renameCol=dfConnectionMap["AB"]
    dfConnectionMap.insert(18, "Q", renameCol)
    del dfConnectionMap["AB"]
    renameCol=dfConnectionMap["X"]
    dfConnectionMap.insert(19, "R", renameCol)
    del dfConnectionMap["X"]
    renameCol=dfConnectionMap["Y"]
    dfConnectionMap.insert(20, "S_20", renameCol)
    del dfConnectionMap["Y"]
    dfConnectionMap=pd.merge(dfConnectionMap, dfCablink4000, left_on="Numbers", right_on="Numbers", how="outer")
    renameCol=dfConnectionMap["S"]
    dfConnectionMap.insert(21, "T18", renameCol)
    del dfConnectionMap["S"]
    del dfConnectionMap["T"]
    renameCol=dfConnectionMap["V"]
    dfConnectionMap.insert(22, "T", renameCol)
    del dfConnectionMap["V"]
    renameCol=dfConnectionMap["W"]
    dfConnectionMap.insert(23, "U", renameCol)
    del dfConnectionMap["W"]
    renameCol=dfConnectionMap["AC"]
    dfConnectionMap.insert(24, "V", renameCol)
    del dfConnectionMap["AC"]
    renameCol=dfConnectionMap["AB"]
    dfConnectionMap.insert(25, "W", renameCol)
    del dfConnectionMap["AB"]
    dfConnectionMap = dfConnectionMap.reindex(columns=["Numbers", "B18", "B", "C", "D", "E", "F", "G", "H18", "H", "I", "J", "K", "L", "M", "N18", "N", "O", "P", "Q", "R", "S_20", "T18", "T", "U", "V", "W", "X", "Y"])
    #print(dfConnectionMap)
    listStart, sublistsTemp, listsTemp, dfConnectionMap, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfConnectionMap, len(dfConnectionMap.columns), 18, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfSite = funcMysqlPandas("nokia_site", pd.DataFrame())
    dfSite = dfSite.loc[dfSite["A"] == sublistSite[5]]
    dfSite["RDB"] = sublistSite[7]
    dfSite["Region"] = sublistSite[3]
    dfSite["UTC"] = sublistSite[23] 
    dfSite["MSW"] = sublistSite[24]
    dfSite["ipPlan"] = sublistSite[25]
    listStart, sublistsTemp, listsTemp, dfSite, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfSite, len(dfSite.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfWcel = funcMysqlPandas("nokia_wcel", pd.DataFrame())
    copyCol=dfWcel["B"]
    dfWcel.insert(0, "Site", copyCol)
    dfWcel["Site"] = dfWcel["Site"].str[:6]
    dfWcel = dfWcel.loc[dfWcel["Site"] == sublistSite[9]]
    #print(dfWcel)

    dfSheet, dfBts = funcMysqlPandas("nokia_bts", pd.DataFrame())
    dfBts = dfBts.loc[dfBts["AE"] == sublistSite[5]]
    #print(dfBts)

    listBscName = [ip.strip() for ip in (settings.CONFIG_DATA.get("LISTBSCNAME")).replace("', '", ",").replace("'", "").split(',')]
    listBscDn = [ip.strip() for ip in (settings.CONFIG_DATA.get("LISTBSCDN")).replace("', '", ",").replace("'", "").split(',')]
    listBscOam = [ip.strip() for ip in (settings.CONFIG_DATA.get("LISTBSCOAM")).replace("', '", ",").replace("'", "").split(',')]
    dfBscRncName["BSC/RNCname"] = listBscName
    dfBscRncName["dn"] = listBscDn
    dfBscRncName["OAM"] = listBscOam
    #print(dfBscRncName)

    dfTemp1 = dfWcel.reindex(columns=["Site", "V", "D", "E", "I"])
    dfTemp2 = dfBts.reindex(columns=["AR", "AJ"])
    dfTemp1=dfTemp1.head(1)
    dfTemp2=dfTemp2.head(1) 
    dfTemp1["Numbers"] = listNumbers[:len(dfTemp1)]
    dfTemp2["Numbers"] = listNumbers[:len(dfTemp2)]
    dfRanData = pd.merge(dfTemp1, dfTemp2, left_on="Numbers", right_on="Numbers", how="outer")
    dfRanData = pd.merge(dfRanData, dfBscRncName, left_on="V", right_on="BSC/RNCname", how="outer")
    dfRanData = dfRanData.dropna() 
    dfRanData = pd.merge(dfRanData, dfBscRncName, left_on="AJ", right_on="BSC/RNCname", how="outer")
    dfRanData = dfRanData.dropna() 
    dfRanData = dfRanData.reindex(columns=["V", "dn_x", "AJ", "dn_y", "D", "E", "I"])
    listStart, sublistsTemp, listsTemp, dfRanData, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfRanData, len(dfRanData.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfAdd = funcMysqlPandas("nokia_add", pd.DataFrame())
    dfAdd2g = dfAdd.loc[dfAdd["A"] == sublistSite[5]]
    dfAdd3g = dfAdd.loc[dfAdd["C"] == sublistSite[5]]
    dfAdd4g = dfAdd.loc[dfAdd["E"] == sublistSite[5]]
    copyCol=dfAdd2g["A"]
    dfAdd2g.insert(0, "Site", copyCol)
    copyCol=dfAdd3g["C"]
    dfAdd3g.insert(0, "Site", copyCol)
    copyCol=dfAdd4g["E"]
    dfAdd4g.insert(0, "Site", copyCol)
    copyCol=dfAdd2g["B"]
    dfAdd2g.insert(0, "Info", copyCol)
    copyCol=dfAdd3g["D"]
    dfAdd3g.insert(0, "Info", copyCol)
    copyCol=dfAdd4g["F"]
    dfAdd4g.insert(0, "Info", copyCol)
    dfAdd2g = dfAdd2g.reindex(columns=["Site", "Info"])
    dfAdd3g = dfAdd3g.reindex(columns=["Site", "Info"])
    dfAdd4g = dfAdd4g.reindex(columns=["Site", "Info"])
    if checkTable(dfAdd2g) == True:
        dfAdd2g["Site"] = [""]
        dfAdd2g["Info"] = [""]
    if checkTable(dfAdd3g) == True:
        dfAdd3g["Site"] = [""]
        dfAdd3g["Info"] = [""]
    if checkTable(dfAdd4g) == True:
        dfAdd4g["Site"] = [""]
        dfAdd4g["Info"] = [""]
    dfAddInfo = pd.concat([dfAdd2g, dfAdd3g])
    dfAddInfo = pd.concat([dfAddInfo, dfAdd4g])
    listStart, sublistsTemp, listsTemp, dfAddInfo, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfAddInfo, len(dfAddInfo.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfMrbts = funcMysqlPandas("nokia_mrbts", pd.DataFrame())
    dfMrbts0000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[4])]    
    dfMrbts3000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[10])]    
    dfMrbts6000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[13])]    
    dfMrbts4000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[16])]
    dfMrbts = pd.concat([dfMrbts0000, dfMrbts3000])
    dfMrbts = pd.concat([dfMrbts, dfMrbts6000])
    dfMrbts = pd.concat([dfMrbts, dfMrbts4000])

    dfSheet, dfEthlk = funcMysqlPandas("nokia_ethlk", pd.DataFrame())
    dfEthlk0000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[4])]    
    dfEthlk3000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[10])]    
    dfEthlk6000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[13])]    
    dfEthlk4000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[16])]
    dfEthlk = pd.concat([dfEthlk0000, dfEthlk3000])
    dfEthlk = pd.concat([dfEthlk, dfEthlk6000])
    dfEthlk = pd.concat([dfEthlk, dfEthlk4000])
    dfDuName = pd.merge(dfMrbts, dfEthlk, left_on="E", right_on="F", how="outer")
    dfDuName = dfDuName.reindex(columns=["E_x", "C_x", "D_y", "H_y", "H_x"])
    dfDuName["E_x"] = dfDuName["E_x"].astype("int64")
    dfDuName["dn"] = "PLMN-PLMN/MRBTS-" + dfDuName["E_x"].astype(str)    
    dfDuName["getRet"] = "any::com.nokia.srbts:MRBTS [ instance() = '" + dfDuName["E_x"].astype(str) + "'] / descendant::com.nokia.srbts.eqm:RETU"
    listStart, sublistsTemp, listsTemp, dfDuName, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfDuName, len(dfDuName.columns), 0, sublistSite[5])
    listStart.append(listsTemp)
    
    sublistConnectionMap.append(sublistSite[4])
    sublistConnectionMap.append(sublistSite[10])
    sublistConnectionMap.append(sublistSite[13])
    sublistConnectionMap.append(sublistSite[16])
    listConnectionMap.append(sublistConnectionMap)
    listStart.append(listConnectionMap)
    return reg, numb, listStart
def funcNokia4gList(reg, numb, list4g):
    sublistSite = []
    listSite = []
    list4g = []
    lenObjs = 0

    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    list4g.append(listSite)

    dfSheet, dfLncel = funcMysqlPandas("nokia_lncel", pd.DataFrame())
    copyCol=dfLncel["B"]
    dfLncel.insert(0, "Site", copyCol)
    dfLncel["Site"] = dfLncel["Site"].str[:6]
    dfLncel = dfLncel.loc[dfLncel["Site"] == sublistSite[5]]
    dfLncel["V"] = dfLncel["V"].astype("int64")
    dfLncel["W"] = dfLncel["W"].astype("int64")
    dfLncel["V"] = dfLncel["V"].astype("str")
    dfLncel["W"] = dfLncel["W"].astype("str")
    dfLncel["LNHOIF_0"] = sublistSite[17]
    dfLncel["LNHOIF_1"] = sublistSite[18]
    dfLncel["LNHOIF_2"] = sublistSite[19]
    dfLncel["LNHOIF_3"] = sublistSite[20]
    dfLncel["LNHOIF_4"] = sublistSite[21]
    dfLncel["LNHOIF_5"] = sublistSite[22]
    df4g = dfLncel.reindex(columns=["Site", "V", "W", "K", "E", "J", "L", "X", "H", "LNHOIF_0", "LNHOIF_1", "LNHOIF_2", "LNHOIF_3", "LNHOIF_4", "LNHOIF_5", "C", "D", "M", "R", "A"])
    list4g, sublistsTemp, listsTemp, df4g, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list4g, [], [], df4g, len(df4g.columns), 0, sublistSite[5])
    list4g.append(listsTemp)
    return reg, numb, list4g
def funcNokia3gList(reg, numb, list3g):
    sublistSite = []
    listSite = []
    
    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    list3g.append(listSite)

    dfSheet, dfWcel = funcMysqlPandas("nokia_wcel", pd.DataFrame())
    copyCol=dfWcel["B"]
    dfWcel.insert(0, "Site", copyCol)
    dfWcel["Site"] = dfWcel["Site"].str[:6]
    dfWcel30000 = dfWcel.loc[dfWcel["Site"] == sublistSite[9]]
    dfWcel40000 = dfWcel.loc[dfWcel["Site"] == sublistSite[15]]
    dfWcel = pd.concat([dfWcel30000, dfWcel40000])
    dfWcel = dfWcel.reindex(columns=["B", "K", "D", "E", "G", "H", "I", "J", "N", "O", "Q", "A"])
    #print(dfWcel)
    list3g, sublistsTemp, listsTemp, dfWcel, lenObjs, lenList, sublistSite[9] = funcAddListFromTable(list3g, [], [], dfWcel, len(dfWcel.columns), 0, sublistSite[9])
    list3g.append(listsTemp)
    return reg, numb, list3g
def funcNokia2gList(reg, numb, list2g):
    sublistSite = []
    listSite = []

    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    list2g.append(listSite)

    dfSheet, dfBcf = funcMysqlPandas("nokia_bcf", pd.DataFrame())
    dfBcf = dfBcf.loc[dfBcf["B"] == sublistSite[5]]
    #print(dfBcf)

    dfSheet, dfBts = funcMysqlPandas("nokia_bts", pd.DataFrame())
    dfBts = dfBts.loc[dfBts["AE"] == sublistSite[5]]
    #print(dfBts)

    dfSheet, dfTrx = funcMysqlPandas("nokia_trx", pd.DataFrame())
    copyCol=dfTrx["AL"]
    dfTrx.insert(0, "Site", copyCol)
    dfTrx["Site"] = dfTrx["Site"].str[:6]
    dfTrx = dfTrx.loc[dfTrx["Site"] == sublistSite[5]]
    #print(dfTrx)
    
    dfTemp1 = dfBcf.reindex(columns=["B", "Y", "C", "Z", "T", "U", "W", "L", "I"])
    dfTemp2 = dfBts.reindex(columns=["C", "AF", "AG", "AH", "D", "H", "I", "J", "K", "L", "AM", "AO", "O", "AN", "T", "Z", "A"])
    dfTemp3 = dfTrx.reindex(columns=["Site", "B", "AL", "G"])     
    dfTemp3 = dfTemp3.loc[dfTemp3["G"] == "MBCCH"]
    df2g = pd.merge(dfTemp2, dfTemp3, left_on="C", right_on="AL", how="outer")
    df2g = pd.merge(df2g, dfTemp1, left_on="Site", right_on="B", how="outer")
    df2g["SATELL"] = "ZOYW:IUA:" + df2g["L_y"].astype(str) + ":PARAM=AFAST:;"
    df2g["RDIV=N"] = "ZEQM:BTS=" + df2g["AH"].astype(str) + ":RDIV=N;"
    df2g["DENA=Y"] = "ZEQV:BTS=" + df2g["AH"].astype(str) + ":GENA=Y;"
    df2g["CMAX=100"] = "ZEQV:BTS=" + df2g["AH"].astype(str) + ":CMAX=100,;"
    df2g["GPRS"] = "ZEQO:BTS=" + df2g["AH"].astype(str) + ":GPRS:;"
    df2g = df2g.reindex(columns=["C_x", "AF", "Y", "AG", "C_y", "Z_y", "T_y", "U", "W", "L_y", "I_y", "AH", "D", "H", "I_x", "J", "K", "L_x", "B_x", "AM", "AO", "O", "AN", "T_x", "Z_x", "A", "SATELL", "RDIV=N", "DENA=Y", "CMAX=100", "GPRS"])
    list2g, sublistsTemp, listsTemp, df2g, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list2g, [], [], df2g, len(df2g.columns), 0, sublistSite[5])
    list2g.append(listsTemp)
    
    dfSheet, dfGnbcf = funcMysqlPandas("nokia_gnbcf", pd.DataFrame())
    dfGnbcf = dfGnbcf.loc[dfGnbcf["O"] == sublistSite[5]]
    #print(dfGnbcf)

    dfMrtbs = dfGnbcf.reindex(columns=["Q", "R", "S", "T", "U", "V"])
    list2g, sublistsTemp, listsTemp, dfMrtbs, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list2g, [], [], dfMrtbs, len(dfMrtbs.columns), 0, sublistSite[5])
    list2g.append(listsTemp)
    return reg, numb, list2g
def funcNokiaTrxList(reg, numb, listTrx, trx, ncell, bcxu, profile, trxNumber, trxFreq, trx0, trx1, trx2, trx3, trx4, trx5, trx6, trx7):
    sublistSite = []
    listSite = []
    listUsersData = []
    sublistUsersData = []
    
    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    listTrx.append(listSite)

    sublistUsersData.append(trx)
    sublistUsersData.append(ncell)
    sublistUsersData.append(bcxu)
    sublistUsersData.append(profile)
    sublistUsersData.append(trxNumber)
    sublistUsersData.append(trxFreq)
    sublistUsersData.append(trx0)
    sublistUsersData.append(trx1)
    sublistUsersData.append(trx2)
    sublistUsersData.append(trx3)
    sublistUsersData.append(trx4)
    sublistUsersData.append(trx5)
    sublistUsersData.append(trx6)
    sublistUsersData.append(trx7)
    listUsersData.append(sublistUsersData)
    listTrx.append(listUsersData)

    dfSheet, dfTrx = funcMysqlPandas("nokia_trx", pd.DataFrame())
    copyCol=dfTrx["AL"]
    dfTrx.insert(0, "Site", copyCol)
    dfTrx["Site"] = dfTrx["Site"].str[:6]
    dfTrx = dfTrx.loc[dfTrx["Site"] == sublistSite[5]]
    #print(dfTrx)

    dfSheet, dfBts = funcMysqlPandas("nokia_bts", pd.DataFrame())
    dfBts = dfBts.loc[dfBts["AE"] == sublistSite[5]]
    #print(dfBts)

    dfSheet, dfBcf = funcMysqlPandas("nokia_bcf", pd.DataFrame())
    dfBcf = dfBcf.loc[dfBcf["B"] == sublistSite[5]]
    #print(dfBcf)

    dfTrxnumber = pd.merge(dfTrx, dfBts, left_on="AL", right_on="C", how="outer")
    dfTrxnumber = dfTrxnumber.reindex(columns=["X_x", "AL_x", "D_x", "B_x", "F_x", "G_x", "H_x", "I_x", "J_x", "K_x", "L_x", "M_x", "N_x", "C_x", "AF_y", "O_x"])
    dfTrxnumber["trx"] = dfTrxnumber["X_x"].astype(str) + sublistSite[1] + dfTrxnumber["AF_y"].astype(str)#Необходимо проверить типы, после переноса с excel в mysql поменялись типы колонок.
    dfTrxnumber["setSatell"] = "ZOYW:IUA:"+dfTrxnumber["D_x"]+":PARAM="+sublistSite[26]+":;"
    listTrx, sublistsTemp, listsTemp, dfTrxnumber, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listTrx, [], [], dfTrxnumber, len(dfTrxnumber.columns), 0, sublistSite[5])
    listTrx.append(listsTemp)
    #print(listTrx)

    dfTemp1 = dfBcf.reindex(columns=["B", "C", "Z"])
    dfTemp2 = dfTrxnumber.loc[dfTrxnumber["AL_x"] == (sublistSite[5]+ncell)]
    dfTemp2=dfTemp2.head(1)
    dfTemp2["Site"] = dfTemp2["AL_x"].str[:6]
    dfTrxData = pd.merge(dfTemp1, dfTemp2, left_on="B", right_on="Site", how="outer")
    dfTrxData["tsc"] = sublistsTemp[0]#Надо проверить tsc. позможно добавить условие что с trx брал именно по cellId
    dfTrxData["bcxuId"] = sublistUsersData[2]
    dfTrxData["profile"] = sublistUsersData[3]
    dfTrxData["bcf"] = sublistSite[1]
    dfTrxData["bts"] = sublistSite[4]
    dfTrxData["trxNumber"] = sublistUsersData[4]
    dfTrxData["trxName"] = sublistUsersData[0]
    dfTrxData["trxFreq"] = sublistUsersData[5]
    dfTrxData["0"] = sublistUsersData[6]
    dfTrxData["1"] = sublistUsersData[7]
    dfTrxData["2"] = sublistUsersData[8]
    dfTrxData["3"] = sublistUsersData[9]
    dfTrxData["4"] = sublistUsersData[10]
    dfTrxData["5"] = sublistUsersData[11]
    dfTrxData["6"] = sublistUsersData[12]
    dfTrxData["7"] = sublistUsersData[13]
    dfTrxData["trxNumber2"] = int(sublistUsersData[4])+49152
    dfTrxData = dfTrxData.reindex(columns=["B", "X_x", "bcf", "bcxuId", "Z", "profile", "AL_x", "AF_y", "bts", "C", "trxNumber", "trxName", "trxFreq", "tsc", "0", "1", "2", "3", "4", "5", "6", "7", "trxNumber2"])#Надо проверить X_x чтоб сооветсвовал ncell
    #print(dfTrxData)
    listTrx, sublistsTemp, listsTemp, dfTrxData, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listTrx, [], [], dfTrxData, len(dfTrxData.columns), 0, sublistSite[5])
    listTrx.append(listsTemp)
    return reg, numb, listTrx, trx, ncell, bcxu, profile, trxNumber, trxFreq, trx0, trx1, trx2, trx3, trx4, trx5, trx6, trx7
def funcNokiaSshList(reg, numb, listSsh):
    sublistSite = []
    listSite = []
     
    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    listSsh.append(listSite)

    dfSheet, dfMrbts = funcMysqlPandas("nokia_mrbts", pd.DataFrame())
    dfMrbts0000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[4])]    
    dfMrbts3000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[10])]    
    dfMrbts6000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[13])]    
    dfMrbts4000 = dfMrbts.loc[dfMrbts["E"] == float(sublistSite[16])]
    dfMrbts = pd.concat([dfMrbts0000, dfMrbts3000])
    dfMrbts = pd.concat([dfMrbts, dfMrbts6000])
    dfMrbts = pd.concat([dfMrbts, dfMrbts4000])
    #print(dfMrbts)

    dfSheet, dfEthlk = funcMysqlPandas("nokia_ethlk", pd.DataFrame())
    dfEthlk0000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[4])]    
    dfEthlk3000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[10])]    
    dfEthlk6000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[13])]    
    dfEthlk4000 = dfEthlk.loc[dfEthlk["F"] == float(sublistSite[16])]
    dfEthlk = pd.concat([dfEthlk0000, dfEthlk3000])
    dfEthlk = pd.concat([dfEthlk, dfEthlk6000])
    dfEthlk = pd.concat([dfEthlk, dfEthlk4000])
    #print(dfEthlk)

    dfSheet, dfBcf = funcMysqlPandas("nokia_bcf", pd.DataFrame())
    dfBcf = dfBcf.loc[dfBcf["B"] == sublistSite[5]]
    #print(dfBcf)

    dfDuName = pd.merge(dfMrbts, dfEthlk, left_on="E", right_on="F", how="outer")
    dfDuName = dfDuName.reindex(columns=["E_x", "C_x"])
    dfDuName["duName"] = dfDuName["E_x"].astype("int64")
    dfDuName["dn"] = "PLMN-PLMN/MRBTS-" + dfDuName["duName"].astype(str)
    #print(dfDuName)
    listSsh, sublistsTemp, listsTemp, dfDuName, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listSsh, [], [], dfDuName, len(dfDuName.columns), 0, sublistSite[5])
    listSsh.append(listsTemp)

    dfLogin = dfBcf.reindex(columns=["Z"])
    listSsh, sublistsTemp, listsTemp, dfLogin, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listSsh, [], [], dfLogin, len(dfLogin.columns), 0, sublistSite[5])
    listSsh.append(listsTemp)
    return reg, numb, listSsh
def funcNokiaHo24List(reg, numb, listHo24):
    sublistSite = []
    listSite = []

    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    listHo24.append(listSite)

    dfSheet, dfBts = funcMysqlPandas("nokia_bts", pd.DataFrame())
    dfBts = dfBts.loc[dfBts["AE"] == sublistSite[5]]
    #print(dfBts)

    dfHo24 = dfBts.reindex(columns=["C", "A", "H"])
    dfHo24["eArfcn"] = sublistSite[27]
    #print(dfHo24)
    listHo24, sublistsTemp, listsTemp, dfHo24, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listHo24, [], [], dfHo24, len(dfHo24.columns), 0, sublistSite[5])
    listHo24.append(listsTemp)
    return reg, numb, listHo24
def funcNokiaPtx3gList(reg, numb, listPtx3g, ptxMax):
    sublistSite = []
    listSite = []
    sublistUsersData = []
    listUsersData = []
    ptxCPICH = 0

    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    listPtx3g.append(listSite)

    if int(ptxMax) > 43:
        ptxCPICH = 33
    else:
        ptxCPICH = int(ptxMax) - 10
    sublistUsersData.append(ptxMax)
    sublistUsersData.append(str(ptxCPICH))
    listUsersData.append(sublistUsersData)
    listPtx3g.append(listUsersData)

    dfSheet, dfWcel = funcMysqlPandas("nokia_wcel", pd.DataFrame())
    copyCol=dfWcel["B"]
    dfWcel.insert(0, "Site", copyCol)
    dfWcel["Site"] = dfWcel["Site"].str[:6]
    dfWcel30000 = dfWcel.loc[dfWcel["Site"] == sublistSite[9]]
    dfWcel40000 = dfWcel.loc[dfWcel["Site"] == sublistSite[15]]
    dfWcel = pd.concat([dfWcel30000, dfWcel40000])
    #print(dfWcel)

    dfPtxMax = dfWcel.reindex(columns=["B", "A", "N", "O"])
    dfPtxMax["PtxCellMax"] = sublistUsersData[0]
    dfPtxMax["PtxPrimaryCPICH"] = sublistUsersData[1]
    dfPtxMax["PtxHighHSDPAPwr"] = str(float(sublistUsersData[0])-0.5)
    dfPtxMax["PtxTargetPSMax"] = dfPtxMax["PtxHighHSDPAPwr"]
    dfPtxMax["PtxMaxHSDPA"] = dfPtxMax["PtxCellMax"]
    dfPtxMax["PtxTargetPSMin"] = dfPtxMax["PtxHighHSDPAPwr"]
    dfPtxMax["PtxOffset"] = "0.5"
    dfPtxMax["PtxTarget"] = dfPtxMax["PtxHighHSDPAPwr"]
    #print(dfPtxMax)
    listPtx3g, sublistsTemp, listsTemp, dfPtxMax, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listPtx3g, [], [], dfPtxMax, len(dfPtxMax.columns), 0, sublistSite[9])
    listPtx3g.append(listsTemp)
    return reg, numb, listPtx3g, ptxMax
def funcNokiaMassLockList(reg, numb, listMassLock):
    sublistSite = []
    listSite = []
    
    reg, numb, sublistSite = funcNokiaAddSublistSite(reg, numb, sublistSite)
    listSite.append(sublistSite)
    listMassLock.append(listSite)

    dfSheet, dfBts = funcMysqlPandas("nokia_bts", pd.DataFrame())
    dfBts = dfBts.loc[dfBts["AE"] == sublistSite[5]]
    #print(dfBts)

    dfSheet, dfWcel = funcMysqlPandas("nokia_wcel", pd.DataFrame())
    copyCol=dfWcel["B"]
    dfWcel.insert(0, "Site", copyCol)
    dfWcel["Site"] = dfWcel["Site"].str[:6]
    dfWcel30000 = dfWcel.loc[dfWcel["Site"] == sublistSite[9]]
    dfWcel40000 = dfWcel.loc[dfWcel["Site"] == sublistSite[15]]
    dfWcel = pd.concat([dfWcel30000, dfWcel40000])
    #print(dfWcel)

    dfSheet, dfLncel = funcMysqlPandas("nokia_lncel", pd.DataFrame())
    copyCol=dfLncel["B"]
    dfLncel.insert(0, "Site", copyCol)
    dfLncel["Site"] = dfLncel["Site"].str[:6]
    dfLncel = dfLncel.loc[dfLncel["Site"] == sublistSite[5]]
    #print(dfLncel)

    dfTemp1 = dfBts.reindex(columns=["B","A"])
    dfTemp2 = dfWcel.reindex(columns=["B","A"])
    dfTemp3 = dfLncel.reindex(columns=["B","A"])
    dfTemp1["tech"] = "2G"
    dfTemp2["tech"] = "3G"
    dfTemp3["tech"] = "4G"
    dfTemp1["cmdBegin"] = '<managedObject class="BTS" version="BSCFP21B" distName="'
    dfTemp2["cmdBegin"] = '<managedObject class="WCEL" version="mcRNCFP20C" distName="'
    dfTemp3["cmdBegin"] = '<managedObject class="LNCEL" version="xL21B_2105_002" distName="'
    dfTemp1["cmdLock"] = '" id="" operation="update"><p name="adminState">Locked</p></managedObject>'
    dfTemp2["cmdLock"] = '" id="" operation="update"><p name="AdminCellState">Locked</p></managedObject>'
    dfTemp3["cmdLock"] = '" id="" operation="update"><p name="administrativeState">locked</p></managedObject>'
    dfTemp1["cmdUnlock"] = '" id="" operation="update"><p name="adminState">Unlocked</p></managedObject>'
    dfTemp2["cmdUnlock"] = '" id="" operation="update"><p name="AdminCellState">Unlocked</p></managedObject>'
    dfTemp3["cmdUnlock"] = '" id="" operation="update"><p name="administrativeState">unlocked</p></managedObject>'
    dfMassLock = pd.concat([dfTemp1, dfTemp2])
    dfMassLock = pd.concat([dfMassLock, dfTemp3])
    #print(dfMassLock)
    listMassLock, sublistsTemp, listsTemp, dfMassLock, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listMassLock, [], [], dfMassLock, len(dfMassLock.columns), 0, sublistSite[5])
    listMassLock.append(listsTemp)
    return reg, numb, listMassLock
def funcEricssonAddSublistSite(reg, numb, sublist, bb):
    numbFull = ""
    numbReg = "" 
    timeUtc = ""
    timeMsw = ""
    ipPlan = ""
    subnetWork = ""
    satell = ""
    listLnhoif = []
    arfcnMin = 0
    arfcnMax = 0
    eArfcn = ""

    hostRdb = settings.CONFIG_DATA.get("HOSTRDB")
    sublist.append(reg)
    sublist.append(numb)

    numb, numbFull = funcCorrectNumbBS(numb, numbFull)
    reg, numbReg, listLnhoif, timeUtc, timeMsw, ipPlan, arfcnMin, arfcnMax, subnetWork, satell, eArfcn = funcCorrectRegBS(reg, numbReg, listLnhoif, timeUtc, timeMsw, ipPlan, arfcnMin, arfcnMax, subnetWork, satell, eArfcn)

    sublist.append(numbFull)
    sublist.append(numbReg)
    sublist.append(numbReg+numbFull)
    sublist.append(reg+numbFull)
    sublist.append(reg+"00"+numbFull)
    sublist.append("https://"+hostRdb+"/p/list.aspx?op=list&k=c3a5t1r&v=c3a5ts5c1cs9r133&q="+reg+"00"+numbFull)

    sublist.append(numbFull[:0]+"3"+numbFull[0+1:])
    sublist.append(reg+(numbFull[:0]+"3"+numbFull[0+1:]))
    sublist.append(numbReg+(numbFull[:0]+"3"+numbFull[0+1:]))
    
    for indexLnhoif in listLnhoif:
        sublist.append(indexLnhoif)

    sublist.append(timeUtc)
    sublist.append(timeMsw)
    sublist.append(ipPlan)

    sublist.append(reg+numbFull+bb)
    sublist.append(reg+(str(int(numbFull)+3000))+bb)
    sublist.append("TCU_"+reg+numbFull)

    if ("-L" in bb) or ("-BL" in bb):
        bbUnit = 6620
        sublist.append(bbUnit)
    else:
        bbUnit = 6630
        sublist.append(bbUnit)

    sublist.append(str(int(numbFull)+3000))
    sublist.append(reg+(str(int(numbFull)+3000)))
    sublist.append(str(int(numbFull)+4000))
    sublist.append(reg+(str(int(numbFull)+4000)))

    sublist.append(str(arfcnMin))
    sublist.append(str(arfcnMax))
    sublist.append(subnetWork)
    return reg, numb, sublist, bb
def funcEricssonStartList(reg, numb, bb, listStart):
    listSite = []
    sublistSite = []
    listBbHwData = []
    sublistInfo = []
    listNumbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
    listBbLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q"]
    dfNumbers = pd.DataFrame()
    
    reg, numb, sublistSite,bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    listStart.append(listSite)

    dfSheet, dfSite = funcMysqlPandas("ericsson_Site", pd.DataFrame())
    dfSite = dfSite.loc[dfSite["A"] == sublistSite[5]]
    dfSite["RDB"] = sublistSite[7]
    dfSite["Region"] = sublistSite[3]
    dfSite["UTC"] = sublistSite[23] 
    dfSite["MSW"] = sublistSite[24]
    dfSite["ipPlan"] = sublistSite[25]
    #print(dfSite)
    listStart, sublistsTemp, listsTemp, dfSite, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfSite, len(dfSite.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfGeranCell = funcMysqlPandas("ericsson_GeranCell", pd.DataFrame())
    dfGeranCell = dfGeranCell.loc[dfGeranCell["AG"] == sublistSite[5]]
    #print(dfGeranCell)

    dfSheet, dfUtranCell = funcMysqlPandas("ericsson_UtranCell", pd.DataFrame())
    copyCol=dfUtranCell["B"]
    dfUtranCell.insert(0, "Site", copyCol)
    dfUtranCell["Site"] = dfUtranCell["Site"].str[:6]
    dfUtranCell = dfUtranCell.loc[dfUtranCell["Site"] == sublistSite[9]]    
    #print(dfUtranCell)

    dfTemp1 = dfGeranCell.reindex(columns=["A", "I", "AH", "AI"])
    dfTemp2 = dfUtranCell.reindex(columns=["A", "U", "Y"])
    dfTemp1 = dfTemp1.head(1)
    dfTemp2 = dfTemp2.head(1) 
    dfTemp1["Numbers"] = listNumbers[:len(dfTemp1)]
    dfTemp2["Numbers"] = listNumbers[:len(dfTemp2)]
    dfRanData = pd.merge(dfTemp1, dfTemp2, left_on="Numbers", right_on="Numbers", how="outer")
    #print(dfRanData)#Поменял типы, после переноса с excel в sql. нужно проверить
    listStart, sublistsTemp, listsTemp, dfRanData, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfRanData, len(dfRanData.columns), 0, sublistSite[5])
    listStart.append(listsTemp)
    
    dfSheet, dfNtp = funcMysqlPandas("ericsson_NTP", pd.DataFrame())
    dfTemp1 = dfNtp.loc[dfNtp["A"] == sublistSite[5]]
    dfTemp2 = dfNtp.loc[dfNtp["C"] == sublistSite[5]]
    dfTemp1 = dfTemp1.reindex(columns=["A", "B"])
    dfTemp2 = dfTemp2.reindex(columns=["C", "D"])
    dfNtp = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="C", how="outer")
    dfNtp = dfNtp.head(1)
    #print(dfNtp)
    listStart, sublistsTemp, listsTemp, dfNtp, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfNtp, len(dfNtp.columns), 0, sublistSite[5])
    listStart.append(listsTemp)
    
    dfSheet, dfIpPlan = funcMysqlPandas("ericsson_IPPlan", pd.DataFrame())
    dfIpPlan = dfIpPlan.loc[dfIpPlan["G"] == sublistSite[5]]
    #print(dfIpPlan)

    dfIpPlanLine1 = dfIpPlan.head(1)
    dfIpPlanLine1 = dfIpPlanLine1.reindex(columns=["AF", "P", "S", "V", "Y", "AB", "AG", "Q", "T", "W", "Z", "AC", "AE", "O", "R", "U", "X", "AA"])
    #print(dfIpPlanLine1)
    listStart, sublistsTemp, listsTemp, dfIpPlanLine1, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfIpPlanLine1, len(dfIpPlanLine1.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfIpBb = funcMysqlPandas("ericsson_IpBb", pd.DataFrame())
    copyCol=dfIpBb["A"]
    dfIpBb.insert(0, "Site", copyCol)
    dfIpBb["Site"] = dfIpBb["Site"].str[:6]
    dfTemp1 = dfIpBb.loc[dfIpBb["Site"] == sublistSite[5]]
    dfTemp2 = dfIpBb.loc[dfIpBb["Site"] == sublistSite[9]]
    dfIpBb = pd.concat([dfTemp1, dfTemp2])
    #print(dfIpBb)

    dfSheet, dfBBEthPort = funcMysqlPandas("ericsson_BB_EthPort", pd.DataFrame())
    copyCol=dfBBEthPort["A"]
    dfBBEthPort.insert(0, "Site", copyCol)
    dfBBEthPort["Site"] = dfBBEthPort["Site"].str[:6]
    dfTemp1 = dfBBEthPort.loc[dfBBEthPort["Site"] == sublistSite[5]]
    dfTemp2 = dfBBEthPort.loc[dfBBEthPort["Site"] == sublistSite[9]]
    dfBBEthPort = pd.concat([dfTemp1, dfTemp2])
    #print(dfBBEthPort)

    dfDuData = pd.merge(dfIpBb, dfBBEthPort, left_on="A", right_on="A", how="outer")
    dfDuData = dfDuData.reindex(columns=["A", "H", "C_y", "F_y"])
    #print(dfDuData)
    listStart, sublistsTemp, listsTemp, dfDuData, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfDuData, len(dfDuData.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    dfSheet, dfIpTcu = funcMysqlPandas("ericsson_IpTcu", pd.DataFrame())
    dfIpTcu = dfIpTcu.loc[dfIpTcu["A"] == sublistSite[28]]
    #print(dfIpTcu)
    listStart, sublistsTemp, listsTemp, dfIpTcu, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfIpTcu, len(dfIpTcu.columns), 0, sublistSite[5])
    listStart.append(listsTemp)
    
    dfSheet, dfProductData = funcMysqlPandas("ericsson_productData", pd.DataFrame())
    copyCol=dfProductData["A"]
    dfProductData.insert(1, "Site", copyCol)
    dfProductData["Site"] = dfProductData["Site"].str[:6]
    dfTemp1 = dfProductData.loc[dfProductData["Site"] == sublistSite[5]]
    dfTemp2 = dfProductData.loc[dfProductData["Site"] == sublistSite[9]]    
    dfProductData = pd.concat([dfTemp1, dfTemp2])
    #print(dfProductData)

    dfProductData1 = dfProductData[~dfProductData["J"].str.startswith("Baseband")]
    dfProductData1 = dfProductData1.sort_values(by='K', ascending=True)
    dfProductData1 = dfProductData1.reindex(columns=["A", "J", "K", "M", "N", "O", "P"])
    dfProductData2 = dfProductData[dfProductData["J"].str.startswith("Baseband")]
    dfProductData2 = dfProductData2.reindex(columns=["A", "J", "K", "M", "N", "O", "P"])
    #print(dfProductData1)
    #print(dfProductData2)

    dfSheet, dfRiLink = funcMysqlPandas("ericsson_RiLink", pd.DataFrame())
    dfRiLink = dfRiLink.reindex(columns=["A", "C", "L"])
    copyCol=dfRiLink["A"]
    dfRiLink.insert(1, "Site", copyCol)
    dfRiLink["Site"] = dfRiLink["Site"].str[:6]    
    dfTemp1 = dfRiLink.loc[dfRiLink["Site"] == sublistSite[5]]
    dfTemp2 = dfRiLink.loc[dfRiLink["Site"] == sublistSite[9]]    
    dfRiLink = pd.concat([dfTemp1, dfTemp2])
    #print(dfRiLink)

    dfBbHwdata = pd.merge(dfProductData2, dfRiLink, left_on="A", right_on="A", how="outer")
    dfProductData2 = dfProductData2.reindex(columns=["A", "J"])
    if checkTable(dfProductData2) == False:
        listNameBB = dfProductData2.values.tolist()#Думаю можно заменить listNameBB на listProductData2
        for nodeId in listNameBB:
            dfRadioXX = dfBbHwdata.loc[dfBbHwdata["A"] == nodeId[0]]#Думаю можно заменить dfRadioXX на dfBbHwdata
            dfRadioXX = dfRadioXX.sort_values(by="C", ascending=True)
            dfRadioXX = dfRadioXX.reindex(columns=["C","L"])
            dfRadioXX2 = dfProductData1.loc[dfProductData1["A"] == nodeId[0]]#Думаю можно заменить dfRadioXX2 на dfProductData1
            dfRadioXX2 = dfRadioXX2.reindex(columns=["K","M","N","O","P"])
            dfNumbers["C"] = listNumbers[0:15]
            dfNumbers["K"] = listBbLetters[0:15]
            dfRadioXX = pd.merge(dfNumbers, dfRadioXX, left_on="C", right_on="C", how="outer")
            dfRadioXX = pd.merge(dfRadioXX, dfRadioXX2, left_on="K", right_on="K", how="outer")
            pd.set_option("future.no_silent_downcasting", True)
            dfRadioXX.fillna("", inplace=True)
            dfRadioXXM = dfRadioXX.reindex(columns=["M"])
            dfRadioXXM = dfRadioXXM.T
            dfRadioXXN = dfRadioXX.reindex(columns=["N"])
            dfRadioXXN = dfRadioXXN.T
            dfRadioXXO = dfRadioXX.reindex(columns=["O"])
            dfRadioXXO = dfRadioXXO.T
            dfRadioXXP = dfRadioXX.reindex(columns=["P"])
            dfRadioXXP = dfRadioXXP.T
            dfRadioXX = dfRadioXX.reindex(columns=["L"])
            dfRadioXX = dfRadioXX.T
            if (checkTable(dfRadioXX) == False) and (checkTable(dfRadioXXM) == False) and (checkTable(dfRadioXXN) == False) and (checkTable(dfRadioXXO) == False) and (checkTable(dfRadioXXP) == False):
                listBbHw= []#Думаю можно переименовать listBbHw на listTemp                
                listRadioXX = dfRadioXX.values.tolist()
                listRadioXXM = dfRadioXXM.values.tolist()
                listRadioXXN = dfRadioXXN.values.tolist()
                listRadioXXO = dfRadioXXO.values.tolist()
                listRadioXXP = dfRadioXXP.values.tolist()
                listBbHw.append(nodeId[0])
                listBbHw.append(nodeId[1])
                for radioXX in listRadioXX[0]:
                    listBbHw.append(radioXX)
                for radioXX in listRadioXXM[0]:
                    listBbHw.append(radioXX)
                for radioXX in listRadioXXN[0]:
                    listBbHw.append(radioXX)
                for radioXX in listRadioXXO[0]:
                    listBbHw.append(radioXX)
                for radioXX in listRadioXXP[0]:
                    listBbHw.append(radioXX)
                listBbHwData.append(listBbHw) 
                #print(listBbHwData)
            else:
                print("- There is no data "+sublistSite[5]+" in the Er_Data file sheet RadioXX from table (dfRadioXX)")
    else:
        print("- There is no data "+sublistSite[5]+" in the Er_Data file sheet RadioXX from table (dfRadioXX)")
        listBbHwData = [["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]
        print(listBbHwData)
    #print(listBbHwData)
    listStart.append(listBbHwData)

    dfSheet, dfAdd = funcMysqlPandas("ericsson_add", pd.DataFrame())
    dfAdd = dfAdd.loc[dfAdd["A"] == sublistSite[5]]
    #print(dfAdd)
   
    dfAddInfo = pd.merge(dfAdd, dfSite, left_on="A", right_on="A", how="outer")
    dfAddInfo = dfAddInfo.reindex(columns=["A", "B_x", "G"])
    #print(dfAddInfo)
    listStart, sublistsTemp, listsTemp, dfAddInfo, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfAddInfo, len(dfAddInfo.columns), 0, sublistSite[5])
    listStart.append(listsTemp)

    if len(listStart[2]) == 0:
        sublistInfo.append("")
    else:
        for listIndex in listStart[2]:            
            sublistInfo.append(listIndex[0])

    dfSheet, dfHw2g = funcMysqlPandas("ericsson_HW_2G", pd.DataFrame())
    dfHw2g = dfHw2g.loc[dfHw2g["M"] == (sublistInfo[0]+"_OTG-"+sublistSite[1])]
    #print(dfHw2g)

    dfDuHwData = dfHw2g.reindex(columns=["M", "O", "U"])
    #dfDuHwData = dfDuHwData[~dfDuHwData["U"].str.startswith("False")]#Заменил на 0, после перенос с excel в sql
    dfDuHwData = dfDuHwData[~dfDuHwData["U"].str.startswith("0")]
    dfDuHwData = dfDuHwData.drop_duplicates()
    dfDuHwData["U"] = dfDuHwData["U"].astype("int64")
    choselistNumbers, dfNumbers = funcAddNumbers(listNumbers[0:9], dfNumbers)
    dfDuHwData = pd.merge(dfDuHwData, dfNumbers, left_on="U", right_on="Numbers", how="outer")
    dfDuHwData = dfDuHwData.drop([4, 5, 6, 7])
    dfDuHwData = dfDuHwData.reindex(columns=["O"])
    dfDuHwData = dfDuHwData.T
    dfDuHwData = dfDuHwData.set_axis(['1', '2', '3', '4', 'DU'], axis=1)
    dfDuHwData["Name"] = sublistInfo[0]+"_OTG-"+sublistSite[1]
    listStart, sublistsTemp, listsTemp, dfDuHwData, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listStart, [], [], dfDuHwData, len(dfDuHwData.columns), 0, sublistSite[5])
    listStart.append(listsTemp)
    return reg, numb, bb, listStart
def funcEricsson4gList(reg, numb, bb, list4g):
    sublistSite = []
    listSite = []
    listNumbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
    listBbLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q"]
    listSectorLte = {"LTE": ["1800", "1800", "1800", "1800", "1800", "1800", "2600", "2600", "2600", "800", "800", "800", "2300", "2300", "2300", "2300", "2300", "2300", "2100", "2100", "2100"], "Sector": ["011", "012", "013", "014", "015", "016", "021", "022", "023", "081", "082", "083", "031", "032", "033", "034", "035", "036", "051", "052", "053"]}
    dfNumbers = pd.DataFrame()

    reg, numb, sublistSite, bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    list4g.append(listSite)

    dfSheet, dfBBEthPort = funcMysqlPandas("ericsson_BB_EthPort", pd.DataFrame())
    dfBBEthPort = dfBBEthPort.loc[dfBBEthPort["A"] == sublistSite[26]]
    #print(dfBBEthPort)

    dfSheet, dfIpPlan = funcMysqlPandas("ericsson_IPPlan", pd.DataFrame())
    dfIpPlan = dfIpPlan.loc[dfIpPlan["I"] == sublistSite[26]]
    #print(dfIpPlan)

    dfSheet, dfNtp = funcMysqlPandas("ericsson_NTP", pd.DataFrame())
    dfTemp1 = dfNtp.loc[dfNtp["A"] == sublistSite[5]]
    dfTemp2 = dfNtp.loc[dfNtp["C"] == sublistSite[5]]
    dfTemp1 = dfTemp1.reindex(columns=["A", "B"])
    dfTemp2 = dfTemp2.reindex(columns=["C", "D"])
    dfNtp = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="C", how="outer")
    dfNtp = dfNtp.head(1)
    #print(dfNtp)
    
    dfTemp1 = dfBBEthPort.reindex(columns=["A", "C"])
    dfTemp2 = dfIpPlan.reindex(columns=["I", "R", "S", "T"])
    dfTemp3 = dfNtp.reindex(columns=["A", "B", "D"])
    dfHardwarePart = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="I", how="outer")
    copyCol=dfHardwarePart["A"]
    dfHardwarePart.insert(0, "Site", copyCol)
    dfHardwarePart["Site"] = dfHardwarePart["Site"].str[:6]
    dfHardwarePart = pd.merge(dfHardwarePart, dfTemp3, left_on="Site", right_on="A", how="outer")
    dfHardwarePart["Reg"] = sublistSite[0]
    #dfHardwarePart["BsName"] = sublistSite[26]
    dfHardwarePart["SiteName"] = sublistSite[5]
    dfHardwarePart["OSS"] = "ENM11"
    dfHardwarePart["MCC"] = "250"
    dfHardwarePart["MNC"] = "20"
    dfHardwarePart["bbUnit"] = sublistSite[29]
    #dfHardwarePart["OSSSiteName"] = sublistSite[5]
    dfHardwarePart = dfHardwarePart.reindex(columns=["Reg", "I", "Site", "OSS", "MCC", "MNC", "bbUnit", "C", "S", "T", "R", "B", "D"])
    list4g, sublistsTemp, listsTemp, dfHardwarePart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list4g, [], [], dfHardwarePart, len(dfHardwarePart.columns), 15, sublistSite[5])
    list4g.append(listsTemp)

    dfSheet, dfProductData = funcMysqlPandas("ericsson_productData", pd.DataFrame())
    dfProductData = dfProductData.loc[dfProductData["A"] == sublistSite[26]]
    #print(dfProductData)

    dfSheet, dfRiLink = funcMysqlPandas("ericsson_RiLink", pd.DataFrame())
    dfRiLink = dfRiLink.loc[dfRiLink["A"] == sublistSite[26]]
    dfRiLink = dfRiLink.reindex(columns=["C", "I"])
    choselistNumbers, dfNumbers = funcAddNumbers(listNumbers[0:15], dfNumbers)
    dfNumbers["L"] = listBbLetters[0:15]
    dfHardwarePart = dfProductData[~dfProductData["J"].str.startswith("Baseband")]
    dfHardwarePart = dfHardwarePart.sort_values(by="K", ascending=True)
    dfHardwarePart = dfHardwarePart.reindex(columns=["A", "K", "M", "N", "O", "P"])
    dfHardwarePart = pd.merge(dfHardwarePart, dfRiLink, left_on="K", right_on="I", how="outer")
    dfHardwarePart = pd.merge(dfNumbers, dfHardwarePart, left_on="Numbers", right_on="C", how="outer")
    dfHardwarePart.fillna("", inplace=True)
    dfHardwarePart["Sector"] = "S" + dfHardwarePart["Numbers"].astype(str)
    dfHardwarePart["RRU"] = "BB Port " + dfHardwarePart["L"]
    condition = (dfHardwarePart["P"].astype(str) == "0") | (dfHardwarePart["P"].astype(str) == "0.0")
    dfHardwarePart.loc[condition, "RfSharing"] = "False"
    dfHardwarePart.loc[~condition, "RfSharing"] = "True" # Используем тильду (~) для инвертирования условия для блока else
    dfHardwarePart = dfHardwarePart.reindex(columns=["Sector", "RRU", "M", "N", "O", "RfSharing"])
    list4g, sublistsTemp, listsTemp, dfHardwarePart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list4g, [], [], dfHardwarePart, len(dfHardwarePart.columns), 15, sublistSite[5])
    list4g.append(listsTemp)

    dfSheet, dfEUtrancellxDD = funcMysqlPandas("ericsson_EUtrancellxDD", pd.DataFrame())
    dfEUtrancellxDD = dfEUtrancellxDD.loc[dfEUtrancellxDD["A"] == sublistSite[26]]
    #print(dfEUtrancellxDD)

    dfSheet, dfSectorCarrier = funcMysqlPandas("ericsson_SectorCarrier", pd.DataFrame())
    dfSectorCarrier = dfSectorCarrier.loc[dfSectorCarrier["A"] ==  sublistSite[26]]
    #print(dfSectorCarrier)

    df4GPart = dfIpPlan.reindex(columns=["AB", "AC", "AA"])
    df4GPart["Region"] = sublistSite[3]
    df4GPart["enB"] = sublistSite[1]
    df4GPart = df4GPart.reindex(columns=["Region", "enB",  "AB", "AC", "AA"])
    list4g, sublistsTemp, listsTemp, df4GPart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list4g, [], [], df4GPart, len(df4GPart.columns), 20, sublistSite[5])
    list4g.append(listsTemp)
    dflistSectorLte = pd.DataFrame(listSectorLte)
    df4GPart = pd.merge(dfEUtrancellxDD, dfSectorCarrier, left_on="B", right_on="C", how="outer")
    copyCol=df4GPart["B_x"]
    df4GPart.insert(0, "Sector", copyCol)
    df4GPart["Sector"] = df4GPart["Sector"].str[7:10]
    df4GPart = pd.merge(dflistSectorLte, df4GPart, left_on="Sector", right_on="Sector", how="outer")
    df4GPart = df4GPart.reindex(columns=["LTE", "AA", "N", "B_x", "G_x", "L", "U", "M", "H_y"])
    #print(sublistSite[11:22])
    #print(sublistSite[11]+","+sublistSite[12]+","+sublistSite[13]+","+sublistSite[14]+","+sublistSite[15]+","+sublistSite[16]+","+sublistSite[17]+","+sublistSite[18]+","+sublistSite[19]+","+sublistSite[20]+","+sublistSite[21]+","+sublistSite[22])
    df4GPart["earfcnDl"] = sublistSite[11]+","+sublistSite[12]+","+sublistSite[13]+","+sublistSite[14]+","+sublistSite[15]+","+sublistSite[16]+","+sublistSite[17]+","+sublistSite[18]+","+sublistSite[19]+","+sublistSite[20]+","+sublistSite[21]+","+sublistSite[22]
    #print(df4GPart)
    list4g, sublistsTemp, listsTemp, df4GPart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list4g, [], [], df4GPart, len(df4GPart.columns), 20, sublistSite[5])
    list4g.append(listsTemp)

    dfSheet, dfGeranCell = funcMysqlPandas("ericsson_GeranCell", pd.DataFrame())
    dfGeranCell = dfGeranCell.loc[dfGeranCell["AG"] == sublistSite[5]]
    #print(dfGeranCell)

    dfTemp1 = dfGeranCell.assign(Numbers = listNumbers[0:len(dfGeranCell)])
    dfTemp2 = df4GPart.assign(Numbers = listNumbers[0:len(df4GPart)])
    dfHo42 = pd.merge(dfTemp1, dfTemp2, left_on="Numbers", right_on="Numbers", how="outer")
    #dfHo42["CGI"] = dfHo42["H"].str[0:3] + dfHo42["H"].str[4:6] + "-" + dfHo42["I"] + "-" + dfHo42["AF"]#поменял, так как после перенос с excel на sql ругался на тип float
    dfHo42["CGI"] = dfHo42["H"].str[0:3] + dfHo42["H"].str[4:6] + "-" + dfHo42["I"].astype(str).str[0:5] + "-" + dfHo42["AF"].astype(str).str[0:2]
    dfHo42["GSMCell"] = dfHo42["E"].str[:6] + "_" + dfHo42["E"].str[6:7]
    dfHo42["SubnetWork"] = sublistSite[36]
    dfHo42["LAC"] = dfHo42["I"]
    dfHo42["eNodeB"] = sublistSite[26]
    dfHo42 = dfHo42.reindex(columns=["SubnetWork", "eNodeB", "B_x", "I", "GSMCell", "CGI", "AF", "AH", "AI", "LAC", "F", "P", "G"])
    #print(dfHo42)
    list4g, sublistsTemp, listsTemp, dfHo42, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list4g, [], [], dfHo42, len(dfHo42.columns), 21, sublistSite[5])
    list4g.append(listsTemp)
    return reg, numb, bb, list4g
def funcEricsson3gList(reg, numb, bb, list3g):
    listSite = []
    sublistSite = []
    listNumbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
    ListUsedSectors = ["S1","S2","S3","S1","S2","S3","S1","S2","S3","S1","S2","S3","S1","S2","S3","S1","S2","S3"]
    dfNumbers = pd.DataFrame()
    
    reg, numb, sublistSite, bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    list3g.append(listSite)

    dfSheet, dfBBEthPort = funcMysqlPandas("ericsson_BB_EthPort", pd.DataFrame())
    dfBBEthPort = dfBBEthPort.loc[dfBBEthPort["A"] == sublistSite[27]]
    #print(dfBBEthPort)

    dfSheet, dfIpPlan = funcMysqlPandas("ericsson_IPPlan", pd.DataFrame())
    dfIpPlan = dfIpPlan.loc[dfIpPlan["I"] == sublistSite[26]]
    #dfIpPlan = dfIpPlan.loc[dfIpPlan["G"] == sublistSite[5]]
    dfIpPlan["Site"] = sublistSite[27]
    #print(dfIpPlan)

    dfSheet, dfNtp = funcMysqlPandas("ericsson_NTP", pd.DataFrame())
    dfTemp1 = dfNtp.loc[dfNtp["A"] == sublistSite[5]]
    dfTemp2 = dfNtp.loc[dfNtp["C"] == sublistSite[5]]
    dfTemp1 = dfTemp1.reindex(columns=["A", "B"])
    dfTemp2 = dfTemp2.reindex(columns=["C", "D"])
    dfNtp = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="C", how="outer")
    dfNtp = dfNtp.head(1)
    dfNtp["Site"] = sublistSite[27]
    #print(dfNtp)
    
    dfTemp1 = dfBBEthPort.reindex(columns=["A", "C"])
    dfTemp2 = dfIpPlan.reindex(columns=["Site", "O", "P", "Q"])
    dfTemp3 = dfNtp.reindex(columns=["Site", "B", "D"])
    dfHardwarePart = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="Site", how="outer")
    dfHardwarePart = pd.merge(dfHardwarePart, dfTemp3, left_on="Site", right_on="Site", how="outer")
    dfHardwarePart["Reg"] = sublistSite[0]
    dfHardwarePart["SiteName"] = sublistSite[5]
    dfHardwarePart["OSS"] = "ENM11"
    dfHardwarePart["MCC"] = "250"
    dfHardwarePart["MNC"] = "20"
    dfHardwarePart["bbUnit"] = "6620"
    dfHardwarePart = dfHardwarePart.reindex(columns=["Reg", "Site", "SiteName", "OSS", "MCC", "MNC", "bbUnit", "C", "O", "P", "Q", "B", "D"])
    #print(dfHardwarePart)
    list3g, sublistsTemp, listsTemp, dfHardwarePart, lenObjs, lenList, sublistSite[31] = funcAddListFromTable(list3g, [], [], dfHardwarePart, len(dfHardwarePart.columns), 0, sublistSite[31])
    list3g.append(listsTemp)

    dfSheet, dfUtranCell = funcMysqlPandas("ericsson_UtranCell", pd.DataFrame())
    copyCol=dfUtranCell["B"]
    dfUtranCell.insert(0, "Site3G", copyCol)
    dfUtranCell["Site3G"] = dfUtranCell["Site3G"].str[:6]
    dfUtranCell = dfUtranCell.loc[dfUtranCell["Site3G"] == sublistSite[31]]
    #print(dfUtranCell)

    dfIpPlan["Site3G"] = sublistSite[31]    
    df3GPart = pd.merge(dfUtranCell, dfIpPlan, left_on="Site3G", right_on="Site3G", how="outer")
    df3GPart["rbsId"] = sublistSite[30]
    df3GPart = df3GPart.reindex(columns=["rbsId", "Y_y", "Z_y", "X_y", "A_x", "N_x", "L_x", "U_x"])
    df3GPart = df3GPart.head(1)
    #print(df3GPart)
    list3g, sublistsTemp, listsTemp, df3GPart, lenObjs, lenList, sublistSite[31] = funcAddListFromTable(list3g, [], [], df3GPart, len(df3GPart.columns), 0, sublistSite[31])
    list3g.append(listsTemp)

    copyCol=dfUtranCell["B"]
    dfUtranCell.insert(0, "localcellid", copyCol)
    dfUtranCell["localcellid"] = dfUtranCell["localcellid"].str[7]
    dfUtranCell["Power"] = "20"
    listNumbers, dfNumbers = funcAddNumbers(listNumbers[0:18], dfNumbers)
    dfNumbers["Numbers"] = dfNumbers["Numbers"].astype("str")
    dfNumbers["UsedSectors"] = ListUsedSectors
    df3GPart = pd.merge(dfNumbers, dfUtranCell, left_on="Numbers", right_on="localcellid", how="outer")
    df3GPart["Numbers"] = df3GPart["Numbers"].astype("int64")
    df3GPart = df3GPart.sort_values(by="Numbers", ascending=True)
    df3GPart = df3GPart.reindex(columns=["UsedSectors", "B", "H", "J", "I", "localcellid", "Power"])
    #print(df3GPart)
    list3g, sublistsTemp, listsTemp, df3GPart, lenObjs, lenList, sublistSite[31] = funcAddListFromTable(list3g, [], [], df3GPart, len(df3GPart.columns), 18, sublistSite[31])
    list3g.append(listsTemp)
    return reg, numb, bb, list3g
def funcEricsson3gsixList(reg, numb, bb, list3gsix):
    listSite = []
    sublistSite = []
    listNumbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
    ListUsedSectors = ["S1","S2","S3","S1","S2","S3","S1","S2","S3","S1","S2","S3","S1","S2","S3","S1","S2","S3"]
    dfNumbers = pd.DataFrame()

    reg, numb, sublistSite, bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    list3gsix.append(listSite)

    dfSheet, dfBBEthPort = funcMysqlPandas("ericsson_BB_EthPort", pd.DataFrame())
    dfBBEthPort = dfBBEthPort.loc[dfBBEthPort["A"] == sublistSite[27]]
    #print(dfBBEthPort)

    dfSheet, dfIpPlan = funcMysqlPandas("ericsson_IPPlan", pd.DataFrame())
    dfIpPlan = dfIpPlan.loc[dfIpPlan["I"] == sublistSite[26]] #-VV2996 и +BU0002
    #dfIpPlan = dfIpPlan.loc[dfIpPlan["G"] == sublistSite[5]]
    dfIpPlan["Site"] = sublistSite[27]
    #print(dfIpPlan)

    dfSheet, dfNtp = funcMysqlPandas("ericsson_NTP", pd.DataFrame())
    dfTemp1 = dfNtp.loc[dfNtp["A"] == sublistSite[5]]
    dfTemp2 = dfNtp.loc[dfNtp["C"] == sublistSite[5]]
    dfTemp1 = dfTemp1.reindex(columns=["A", "B"])
    dfTemp2 = dfTemp2.reindex(columns=["C", "D"])
    dfNtp = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="C", how="outer")
    dfNtp = dfNtp.head(1)
    dfNtp["Site"] = sublistSite[27]
    #dfNtp["BsName"] = sublistSite[26]
    #print(dfNtp)
    
    dfTemp1 = dfBBEthPort.reindex(columns=["A", "C"])
    dfTemp2 = dfIpPlan.reindex(columns=["Site", "O", "P", "Q", "H"])
    dfTemp3 = dfNtp.reindex(columns=["Site", "B", "D"])
    dfHardwarePart = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="Site", how="outer")
    dfHardwarePart = pd.merge(dfHardwarePart, dfTemp3, left_on="Site", right_on="Site", how="outer")
    dfHardwarePart["Reg"] = sublistSite[0]
    dfHardwarePart["SiteName"] = sublistSite[5]
    dfHardwarePart["OSS"] = "ENM11"
    dfHardwarePart["MCC"] = "250"
    dfHardwarePart["MNC"] = "20"
    dfHardwarePart["bbUnit"] = "6620"
    dfHardwarePart["OssSiteName"] = sublistSite[5]
    dfHardwarePart = dfHardwarePart.reindex(columns=["Reg", "H", "SiteName", "OSS", "MCC", "MNC", "bbUnit", "C", "P", "Q", "O", "B", "D", "OssSiteName"])
    #print(dfHardwarePart)
    list3gsix, sublistsTemp, listsTemp, dfHardwarePart, lenObjs, lenList, sublistSite[9] = funcAddListFromTable(list3gsix, [], [], dfHardwarePart, len(dfHardwarePart.columns), 0, sublistSite[9])
    list3gsix.append(listsTemp)

    dfSheet, dfUtranCell = funcMysqlPandas("ericsson_UtranCell", pd.DataFrame())
    copyCol=dfUtranCell["B"]
    dfUtranCell.insert(0, "Site3G", copyCol)
    dfUtranCell["Site3G"] = dfUtranCell["Site3G"].str[:6]
    copyCol=dfUtranCell["B"]
    dfUtranCell.insert(0, "Site3GS", copyCol)
    dfUtranCell["Site3GS"] = dfUtranCell["Site3GS"].str[:6]
    #dfUtranCell = dfUtranCell.loc[dfUtranCell["Site3G"] == sublistSite[31]]
    dfTemp1 = dfUtranCell.loc[dfUtranCell["Site3G"] == sublistSite[31]]
    dfTemp2 = dfUtranCell.loc[dfUtranCell["Site3GS"] == sublistSite[33]]
    dfUtranCell = pd.concat([dfTemp1, dfTemp2])
    #print(dfUtranCell)

    dfIpPlan["Site3G"] = sublistSite[31]    
    df3GPart = pd.merge(dfUtranCell, dfIpPlan, left_on="Site3G", right_on="Site3G", how="outer")
    df3GPart["rbsId"] = sublistSite[32]
    df3GPart = df3GPart.reindex(columns=["rbsId", "Y_y", "Z_y", "X_y", "A_x", "N_x", "L_x", "U_x"])
    df3GPart = df3GPart.head(1)
    #df3GPart["U_x"] = df3GPart["U_x"].astype("int")
    #print(df3GPart)
    list3gsix, sublistsTemp, listsTemp, df3GPart, lenObjs, lenList, sublistSite[9] = funcAddListFromTable(list3gsix, [], [], df3GPart, len(df3GPart.columns), 0, sublistSite[9])
    list3gsix.append(listsTemp)

    copyCol = dfUtranCell["B"]
    dfUtranCell.insert(0, "localcellid", copyCol)
    dfUtranCell["localcellid"] = dfUtranCell["localcellid"].str[7]
    dfUtranCell["Power"] = "20"
    df3GPart = dfUtranCell.loc[dfUtranCell["Site3GS"] == sublistSite[33]]
    listNumbers, dfNumbers = funcAddNumbers(listNumbers[0:18], dfNumbers)
    dfNumbers["UsedSectors"] = ListUsedSectors
    dfNumbers["Numbers"] = dfNumbers["Numbers"].astype("str")
    df3GPart = pd.merge(dfNumbers, df3GPart, left_on="Numbers", right_on="localcellid", how="outer")
    df3GPart = df3GPart.loc[df3GPart["Site3GS"] == sublistSite[33]]
    df3GPart = df3GPart.reindex(columns=["UsedSectors", "B", "H", "J", "I", "localcellid", "Power"])
    #print(df3GPart)
    list3gsix, sublistsTemp, listsTemp, df3GPart, lenObjs, lenList, sublistSite[9] = funcAddListFromTable(list3gsix, [], [], df3GPart, len(df3GPart.columns), 7, sublistSite[9])
    list3gsix.append(listsTemp)
    return reg, numb, bb, list3gsix
def funcEricsson2gList(reg, numb, bb, list2g):
    listSite = []
    sublistSite = []
    listNullCol = ["","",""]
    listNumbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
    ListUsedSectors = ["S1","S2","S3","S1","S2","S3"]
    dfNumbers = pd.DataFrame()

    reg, numb, sublistSite, bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    list2g.append(listSite)

    dfSheet, dfBBEthPort = funcMysqlPandas("ericsson_BB_EthPort", pd.DataFrame())
    dfBBEthPort = dfBBEthPort.loc[dfBBEthPort["A"] == sublistSite[26]]
    #print(dfBBEthPort)

    dfSheet, dfIpPlan = funcMysqlPandas("ericsson_IPPlan", pd.DataFrame())
    dfIpPlan = dfIpPlan.loc[dfIpPlan["I"] == sublistSite[26]] #-VV2996 и +BU0002
    #dfIpPlan = dfIpPlan.loc[dfIpPlan["G"] == sublistSite[5]]
    #print(dfIpPlan)

    dfSheet, dfNtp = funcMysqlPandas("ericsson_NTP", pd.DataFrame())
    dfTemp1 = dfNtp.loc[dfNtp["A"] == sublistSite[5]]
    dfTemp2 = dfNtp.loc[dfNtp["C"] == sublistSite[5]]
    dfTemp1 = dfTemp1.reindex(columns=["A", "B"])
    dfTemp2 = dfTemp2.reindex(columns=["C", "D"])
    dfNtp = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="C", how="outer")
    dfNtp = dfNtp.head(1)
    dfNtp["Site"] = sublistSite[26]
    #print(dfNtp)
    
    dfTemp1 = dfBBEthPort.reindex(columns=["A", "C"])
    dfTemp2 = dfIpPlan.reindex(columns=["AE", "AF", "AG", "H"])
    dfTemp3 = dfNtp.reindex(columns=["Site", "B", "D"])
    dfHardwarePart = pd.merge(dfTemp1, dfTemp2, left_on="A", right_on="H", how="outer")
    dfHardwarePart = pd.merge(dfHardwarePart, dfTemp3, left_on="H", right_on="Site", how="outer")
    dfHardwarePart["Reg"] = sublistSite[0]
    dfHardwarePart["SiteName"] = sublistSite[5]
    dfHardwarePart["OSS"] = "ENM11"
    dfHardwarePart["MCC"] = "250"
    dfHardwarePart["MNC"] = "20"
    dfHardwarePart["bbUnit"] = "6620"
    dfHardwarePart["OssSiteName"] = sublistSite[5]
    dfHardwarePart = dfHardwarePart.reindex(columns=["Reg", "H", "SiteName", "OSS", "MCC", "MNC", "bbUnit", "C", "AF", "AG", "AE", "B", "D", "OssSiteName"])
    #print(dfHardwarePart)
    list2g, sublistsTemp, listsTemp, dfHardwarePart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list2g, [], [], dfHardwarePart, len(dfHardwarePart.columns), 0, sublistSite[5])
    list2g.append(listsTemp)

    dfSheet, dfGeranCell = funcMysqlPandas("ericsson_GeranCell", pd.DataFrame())
    dfGeranCell = dfGeranCell.loc[dfGeranCell["AG"] == sublistSite[5]]
    #print(dfGeranCell)

    df2GPart = pd.merge(dfGeranCell, dfIpPlan, left_on="AG", right_on="G", how="outer")
    df2GPart = df2GPart.reindex(columns=["AG_x", "V_y", "W_y", "U_y", "A_x"])
    df2GPart = df2GPart.head(1)
    #print(df2GPart)
    list2g, sublistsTemp, listsTemp, df2GPart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list2g, [], [], df2GPart, len(df2GPart.columns), 0, sublistSite[5])
    list2g.append(listsTemp)

    dfSheet, dfChannelGroup = funcMysqlPandas("ericsson_ChannelGroup", pd.DataFrame())
    copyCol=dfChannelGroup["E"]
    dfChannelGroup.insert(1, "Site", copyCol)
    dfChannelGroup["Site"] = dfChannelGroup["Site"].str[:6]
    dfChannelGroup = dfChannelGroup.loc[dfChannelGroup["Site"] == sublistSite[5]]
    #print(dfChannelGroup)

    dfSheet, dfTrx = funcMysqlPandas("ericsson_trx", pd.DataFrame())
    copyCol=dfTrx["C"]
    dfTrx.insert(1, "Site", copyCol)
    dfTrx["Site"] = dfTrx["Site"].str[:6]
    dfTrx = dfTrx.loc[dfTrx["Site"] == sublistSite[5]]
    #print(dfTrx)

    df2gData = dfChannelGroup.reindex(columns=["E", "F", "N", "O", "P", "AU"])
    dfTemp1 = df2gData.loc[df2gData["F"].astype(str) == "1"]#Добавил .astype(str) так как после перенос с excel в sql число 1 видел с типом int64, поэтому не отображались данные
    dfTemp2 = df2gData.loc[df2gData["F"].astype(str)  == "0"]
    if (checkTable(dfTemp1) == True):
        listF = [1,1,1]
        dfTemp1 = dfTemp2.reindex(columns=["E", "N", "O", "AU"])
        dfTemp1["P"] = listNullCol
        dfTemp1["F"] = listF
        dfTemp1 = dfTemp1.reindex(columns=["E", "F", "N", "O", "P", "AU"])
    elif (checkTable(dfTemp2) == True):
        listF = [0,0,0]
        dfTemp2 = dfTemp1.reindex(columns=["E", "N", "O", "AU"])
        dfTemp2["P"] = listNullCol
        dfTemp2["F"] = listF
        dfTemp2 = dfTemp2.reindex(columns=["E", "F", "N", "O", "P", "AU"])
    listCell = [sublistSite[5]+"1", sublistSite[5]+"2", sublistSite[5]+"3"]
    if dfTemp1.shape[0] != len(listNullCol):
        dfTemp=pd.DataFrame(listCell)
        renameCol=dfTemp[0]
        dfTemp.insert(0, "0", renameCol)
        del dfTemp[0]
        dfTemp = pd.merge(dfTemp, dfTemp1, left_on="0", right_on="E", how="outer")
        del dfTemp["E"]
        renameCol=dfTemp["0"]
        dfTemp.insert(0, "E", renameCol)
        del dfTemp["0"]        
        dfTemp.fillna("", inplace=True)
        dfTemp1=dfTemp
    elif dfTemp2.shape[0] != len(listNullCol):
        dfTemp=pd.DataFrame(listCell)
        renameCol=dfTemp[0]
        dfTemp.insert(0, "0", renameCol)
        del dfTemp[0]
        dfTemp = pd.merge(dfTemp, dfTemp2, left_on="0", right_on="E", how="outer")
        del dfTemp["E"]
        renameCol=dfTemp["0"]
        dfTemp.insert(0, "E", renameCol)
        del dfTemp["0"]        
        dfTemp.fillna("", inplace=True)
        dfTemp2=dfTemp
    df2gData = pd.merge(dfTemp1, dfTemp2, left_on="E", right_on="E", how="inner")
    if checkTable(dfTrx) == False:
        listTrx = dfTrx.values.tolist()
        dfTemp = pd.DataFrame(listTrx)
        dfTemp = dfTemp.drop_duplicates(3, keep="first")
        #print(dfTemp[4].dtype)
        if dfTemp[4].dtype == "int64":
            dfTemp[4] = dfTemp[4] + 1
        renameCol=dfTemp[3]
        dfTemp.insert(3, "3", renameCol)
        del dfTemp[3]
        renameCol=dfTemp[0]
        dfTemp.insert(0, "0", renameCol)
        del dfTemp[0]
        renameCol=dfTemp[1]
        dfTemp.insert(1, "1", renameCol)
        del dfTemp[1]
        renameCol=dfTemp[2]
        dfTemp.insert(2, "2", renameCol)
        del dfTemp[2]
        renameCol=dfTemp[4]
        dfTemp.insert(4, "4", renameCol)
        del dfTemp[4]
        dfTrx = dfTemp
    else:
        dfTemp = df2gData
        copyCol=dfTemp["E"]
        dfTemp.insert(1, "3", copyCol)
        dfTemp=dfTemp.reindex(columns=["3"])
        dfTemp["0"] = listNullCol
        dfTemp["1"] = listNullCol
        dfTemp["2"] = listNullCol
        dfTemp["4"] = listNullCol
        dfTrx = dfTemp
    df2gData = pd.merge(df2gData, dfTrx, left_on="E", right_on="3", how="inner")
    df2gData = pd.merge(df2gData, dfGeranCell, left_on="E", right_on="E", how="inner")
    df2gData = df2gData.reindex(columns=["E", "A", "K", "N_y", "O_x", "Y", "P_y", "P_x", "G", "P", "F", "I", "AF", "4", "AU_x", "Q"])
    list2g, sublistsTemp, listsTemp, df2gData, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list2g, [], [], df2gData, len(df2gData.columns), 0, sublistSite[5])
    list2g.append(listsTemp)
    listNumbers, dfNumbers = funcAddNumbers(listNumbers[0:6], dfNumbers)
    dfNumbers["UsedSectors"] = ListUsedSectors
    dfNumbers["Numbers"] = dfNumbers["Numbers"].astype("str")
    copyCol = df2gData["E"]
    df2gData.insert(0, "Site", copyCol)
    df2gData["Site"] = df2gData["Site"].str[:6]
    copyCol = df2gData["E"]
    df2gData.insert(0, "Numbers", copyCol)
    df2gData["Numbers"] = df2gData["Numbers"].str[6:7]
    df2GPart = pd.merge(dfNumbers, df2gData, left_on="Numbers", right_on="Numbers", how="outer")
    df2GPart = df2GPart.loc[df2GPart["Site"] == sublistSite[5]]
    df2GPart["power"] = "20"
    df2GPart["arfcnMin"] = sublistSite[34]
    df2GPart["arfcnMax"] = sublistSite[35]
    df2GPart = df2GPart.reindex(columns=["UsedSectors", "K", "E", "4", "G", "arfcnMin", "arfcnMax","power"])
    #print(df2GPart) 
    list2g, sublistsTemp, listsTemp, df2GPart, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(list2g, [], [], df2GPart, len(df2GPart.columns), 0, sublistSite[5])
    list2g.append(listsTemp)
    return reg, numb, bb, list2g
def funcEricssonLicList(reg, numb, bb, listForJson):
    listSite = []
    sublistSite = []
    listCapacity = []
    listFree = []
    listTotalTrx = []
    listCapacityState = ["CXC4012037","CXC4021010","CXC4011622","CXC4012338"]
    listDescription = ["GSM Cell Carrier (TRX) ERS","WCDMA Number of Cell Carriers","5 MHz Sector Carriers","OutputPower 20W Step"]

    reg, numb, sublistSite, bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    listForJson.append(listSite)

    dfSheet, dfSectorCarrier = funcMysqlPandas("ericsson_SectorCarrier", pd.DataFrame())
    colDf, dfSectorCarrier, sublistSite[5], sublistSite[9] = funcFilterTables24G3G("A", dfSectorCarrier, sublistSite[5], sublistSite[9])
    #print(dfSectorCarrier)

    dfSheet, dfEUtrancellxDD= funcMysqlPandas("ericsson_EUtrancellxDD", pd.DataFrame())
    colDf, dfEUtrancellxDD, sublistSite[5], sublistSite[9] = funcFilterTables24G3G("A", dfEUtrancellxDD, sublistSite[5], sublistSite[9])
    #print(dfEUtrancellxDD)

    dfSheet, dfTrx = funcMysqlPandas("ericsson_trx", pd.DataFrame())
    colDf, dfTrx, sublistSite[5], sublistSite[9] = funcFilterTables24G3G("A", dfTrx, sublistSite[5], sublistSite[9])
    #print(dfTrx)

    dfSheet, dfLicense = funcMysqlPandas("ericsson_License", pd.DataFrame())
    dfTemp1 = dfLicense[["C", "D"]]
    dfTemp1 = dfTemp1[dfTemp1["C"] == sublistSite[26]]
    if dfTemp1.empty:
        print(f"Значение {sublistSite[26]} не найдено. Создаю строку с нулевым значением.")    
        dfTemp1 = pd.DataFrame.from_dict({"C": [sublistSite[26]], "D": [0]})
    else:
        dfTemp1 = dfTemp1
    dfTemp1 = dfTemp1.rename(columns={"C": "BS", "D": "CapacityLevel"})
    dfTemp2 = dfLicense[["G", "H"]]
    dfTemp2 = dfTemp2[dfTemp2["G"] == sublistSite[26]]
    if dfTemp2.empty:
        print(f"Значение {sublistSite[26]} не найдено. Создаю строку с нулевым значением.")    
        dfTemp2 = pd.DataFrame.from_dict({"G": [sublistSite[26]], "H": [0]})
    else:
        dfTemp2 = dfTemp2
    dfTemp2 = dfTemp2.rename(columns={"G": "BS", "H": "CapacityLevel"})
    dfTemp3 = dfLicense[["A", "B"]]
    dfTemp3 = dfTemp3[dfTemp3["A"] == sublistSite[26]]
    if dfTemp3.empty:
        print(f"Значение {sublistSite[26]} не найдено. Создаю строку с нулевым значением.")    
        dfTemp3 = pd.DataFrame.from_dict({"A": [sublistSite[26]], "B": [0]})
    else:
        dfTemp3 = dfTemp3
    dfTemp3 = dfTemp3.rename(columns={"A": "BS", "B": "CapacityLevel"})
    dfTemp4 = dfLicense[["E", "F"]]
    dfTemp4 = dfTemp4[dfTemp4["E"] == sublistSite[26]]
    if dfTemp4.empty:
        print(f"Значение {sublistSite[26]} не найдено. Создаю строку с нулевым значением.")    
        dfTemp4 = pd.DataFrame.from_dict({"E": [sublistSite[26]], "F": [0]})
    else:
        dfTemp4 = dfTemp4
    dfTemp4 = dfTemp4.rename(columns={"E": "BS", "F": "CapacityLevel"})
    dfLicense = pd.concat([dfTemp1, dfTemp2])
    dfLicense = pd.concat([dfLicense, dfTemp3])
    dfLicense = pd.concat([dfLicense, dfTemp4])
    #print(dfLicense)

    dfLteConfiguration = pd.merge(dfSectorCarrier, dfEUtrancellxDD, left_on="C", right_on="B", how="outer")
    dfLteConfiguration = dfLteConfiguration.reindex(columns=["C_x", "H_x", "AA"])
    power = dfLteConfiguration["H_x"].sum()
    lteBandwidth = dfLteConfiguration["AA"].sum()
    dfTemp1 = pd.DataFrame()
    dfTemp1["C_x"] = "Total"
    dfTemp1["H_x"] = power
    dfTemp1["AA"] = lteBandwidth
    dfTemp1 = pd.DataFrame([["Total", power, lteBandwidth]], columns=["C_x", "H_x", "AA"])
    dfLteConfiguration = pd.concat([dfLteConfiguration, dfTemp1])
    #print(dfLteConfiguration)
    listForJson, sublistsTemp, listsTemp, dfLteConfiguration, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listForJson, [], [], dfLteConfiguration, len(dfLteConfiguration.columns), 0, sublistSite[5])
    listForJson.append(listsTemp)

    dfGsmConfiguration = dfTrx.reindex(columns=["C", "B"])
    trx = dfGsmConfiguration["B"].sum()
    dfTemp1 = pd.DataFrame()
    dfTemp1["C"] = "Total"
    dfTemp1 = pd.DataFrame([["Total", trx]], columns=["C", "B"])
    dfGsmConfiguration = pd.concat([dfGsmConfiguration, dfTemp1])
    #print(dfGsmConfiguration)
    listForJson, sublistsTemp, listsTemp, dfGsmConfiguration, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listForJson, [], [], dfGsmConfiguration, len(dfGsmConfiguration.columns), 0, sublistSite[5])
    listForJson.append(listsTemp)

    if checkTable(dfLicense) == False:
        listCapacityLevel = dfLicense["CapacityLevel"].tolist()
        listCapacity.append(listCapacityLevel[0])
        listCapacity.append(listCapacityLevel[1])
        listCapacity.append(listCapacityLevel[2]*5)
        listCapacity.append((listCapacityLevel[3]-listCapacityLevel[1]+3)*20)        
    else:
        listCapacity = ["","","",""]
    if checkTable(dfGsmConfiguration) == False:
        listTotalTrx = dfGsmConfiguration["B"].tolist()        
    else:
        listTotalTrx = ["","","",""]
    if checkTable(dfLteConfiguration) == False:
        listTotalLteBandwidth = dfLteConfiguration.tail(1).values.tolist()[0]       
    else:
        listTotalLteBandwidth = ["","",""]
    if listCapacityLevel[0] + listCapacityLevel[2] + listCapacityLevel[3] == 0:
        listFree.append("9999 TRX")
    else:
        if listCapacity[0] - listTotalTrx[3] < 0:
            listFree.append("0 TRX")
        else:
            listFree.append(str(listCapacity[0] - listTotalTrx[3])+" TRX")
    listFree.append("0")
    if listCapacityLevel[0] + listCapacityLevel[2] + listCapacityLevel[3] == 0:
        listFree.append("9999 MHz")
    else:
        if listCapacity[2] - listTotalLteBandwidth[2] < 0:
            listFree.append("0 MHz")
        else:
            listFree.append(str(listCapacity[2] - listTotalLteBandwidth[2])+" MHz")
    if listCapacityLevel[0] + listCapacityLevel[2] + listCapacityLevel[3] == 0:
        listFree.append("9999 W")
    else:
        if listCapacity[3] - listTotalLteBandwidth[1] < 0:
            listFree.append("0 W")
        else:
            listFree.append(str(listCapacity[3] - listTotalLteBandwidth[1])+" W")
    dfBbLicense = dfLicense.reindex(columns=["CapacityLevel"])
    dfBbLicense["Capacity"] = listCapacity
    dfBbLicense["Free"] = listFree
    dfBbLicense["CapacityState"] = listCapacityState
    dfBbLicense["Description"] = listDescription
    #print(dfBbLicense)
    listForJson, sublistsTemp, listsTemp, dfBbLicense, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listForJson, [], [], dfBbLicense, len(dfBbLicense.columns), 0, sublistSite[5])
    listForJson.append(listsTemp)
    return reg, numb, bb, listForJson
def funcEricssonRetList(reg, numb, bb, listForJson):
    listSite = []
    sublistSite = []

    reg, numb, sublistSite, bb = funcEricssonAddSublistSite(reg, numb, sublistSite, bb)
    listSite.append(sublistSite)
    listForJson.append(listSite)

    dfSheet, dfRet = funcMysqlPandas("ericsson_RET", pd.DataFrame())
    colDf, dfRet, sublistSite[5], sublistSite[9] = funcFilterTables24G3G("G", dfRet, sublistSite[5], sublistSite[9])
    #print(dfRet)
    
    dfRetBS = dfRet.reindex(columns=["G", "H", "K", "M", "S", "W"])
    dfRetBS["cols3"] = dfRetBS["S"].str[8:10]
    dfTemp1 = dfRetBS.loc[dfRetBS["cols3"] == "B1"]
    dfTemp2 = dfRetBS.loc[dfRetBS["cols3"] == "B2"]
    dfTemp3 = dfRetBS.loc[dfRetBS["cols3"] == "B3"]
    dfTemp4 = dfRetBS.loc[dfRetBS["cols3"] == "B4"]
    dfTemp5 = dfRetBS.loc[dfRetBS["cols3"] == "B5"]
    dfTemp6 = dfRetBS.loc[dfRetBS["cols3"] == "B6"]
    dfTemp1 = dfTemp1.rename(columns={"G":"GB1", "K":"KB1", "M":"MB1", "S":"SB1", "W":"WB1", "cols3":"cols3B1"})
    dfTemp2 = dfTemp2.rename(columns={"G":"GB2", "K":"KB2", "M":"MB2", "S":"SB2", "W":"WB2", "cols3":"cols3B2"})
    dfTemp3 = dfTemp3.rename(columns={"G":"GB3", "K":"KB3", "M":"MB3", "S":"SB3", "W":"WB3", "cols3":"cols3B3"})
    dfTemp4 = dfTemp4.rename(columns={"G":"GB4", "K":"KB4", "M":"MB4", "S":"SB4", "W":"WB4", "cols3":"cols3B4"})
    dfTemp5 = dfTemp5.rename(columns={"G":"GB5", "K":"KB5", "M":"MB5", "S":"SB5", "W":"WB5", "cols3":"cols3B5"})
    dfTemp6 = dfTemp6.rename(columns={"G":"GB6", "K":"KB6", "M":"MB6", "S":"SB6", "W":"WB6", "cols3":"cols3B6"})
    dfRetBS = pd.merge(dfTemp1, dfTemp2, left_on="H", right_on="H", how="outer")
    dfRetBS = pd.merge(dfRetBS, dfTemp3, left_on="H", right_on="H", how="outer")
    dfRetBS = pd.merge(dfRetBS, dfTemp4, left_on="H", right_on="H", how="outer")
    dfRetBS = pd.merge(dfRetBS, dfTemp5, left_on="H", right_on="H", how="outer")
    dfRetBS = pd.merge(dfRetBS, dfTemp6, left_on="H", right_on="H", how="outer")
    dfRetBS = dfRetBS.reindex(columns=["GB1", "H", "KB1", "MB1", "WB1", "KB2", "MB2", "WB2", "KB3", "MB3", "WB3", "KB4", "MB4", "WB4", "KB5", "MB5", "WB5", "KB6", "MB6", "WB6"])
    #print(dfRetBS)
    listForJson, sublistsTemp, listsTemp, dfRetBS, lenObjs, lenList, sublistSite[5] = funcAddListFromTable(listForJson, [], [], dfRetBS, len(dfRetBS.columns), 0, sublistSite[5])
    listForJson.append(listsTemp)
    return reg, numb, bb, listForJson
def getDjangoData(request):
    listContents = Content.objects.all()      
    #print(listContents) 
    jsonContents = {}

    for raw in listContents:
        #print(raw.idmenu)
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = [] # Добавить Menu из модели в словарь jsonContents
        jsonContents[raw.idmenu].append({
            'id': raw.id,
            'title': raw.title,
            'content': raw.content,
            'idcard': raw.idcard,
            'idmenu': raw.idmenu,
            'author': raw.author,
            'date': raw.date
        })# Добавить Весь контент из модели в словарь jsonContents
    #print(jsonContents)
    #for j_key, j_value in jsonContents.items():
        #print(j_key) # Отобразить на сайте ключ из словаря jsonContents type - str
        #print(j_value[0]) # Отобразить на сайте значения из словаря jsonContents type - dict
        #print(j_value[0]['idmenu']) # Отобразить на сайте значения idmenu из словаря jsonContents type - str
    #    for item in j_value:
            #print(item['idcard']) # Отобразить на сайте все значения idcard из словаря jsonContents type - str
    #        if item['idcard'] == 'MiniCard':
                #print(item['title'])
                #print(item['content'])            
    #            print("true") # Отобразить на сайте значения title и content из словаря, у которых idcard MiniCard

    combined_context = {
        **{'jsonContents': jsonContents},
        }
    #print(combined_context)
    return render(request, 'index.html', combined_context)
def funcNokiaStart(request):
    jsonContents = {}
    listNokiaStart = []

    listContents = Content.objects.all()      
    #print(listContents)
    for raw in listContents:
        #print(raw.idmenu)
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            'id': raw.id,
            'title': raw.title,
            'content': raw.content,
            'idcard': raw.idcard,
            'idmenu': raw.idmenu,
            'author': raw.author,
            'date': raw.date
        })
    #print(jsonContents)

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokiaStart = funcNokiaStartList(inputReg, inputNumber, listNokiaStart)
        print(listNokiaStart)
        #listNokiaStart, indexList = funcTestingOutList(listNokiaStart, 0)

    combined_context = {
        **{'jsonContents': jsonContents},
        **{'listNokiaStart': listNokiaStart},
        }
    return render(request, 'pageNokiaStart.html', combined_context)
def funcNokia4g(request):
    jsonContents = {}
    listNokia4g = []

    listContents = Content.objects.all()
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokia4g = funcNokia4gList(inputReg, inputNumber, listNokia4g)
        print(listNokia4g)
        #listNokia4g, indexList = funcTestingOutList(listNokia4g, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokia4g": listNokia4g},
        }
    return render(request, "pageNokia4g.html", combined_context)
def funcNokia3g(request):
    jsonContents = {}
    listNokia3g = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokia3g = funcNokia3gList(inputReg, inputNumber, listNokia3g)
        print(listNokia3g)
        #listNokia3g, indexList = funcTestingOutList(listNokia3g, 1)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokia3g": listNokia3g},
        }
    return render(request, "pageNokia3g.html", combined_context)
def funcNokia2g(request):
    jsonContents = {}
    listNokia2g = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokia2g = funcNokia2gList(inputReg, inputNumber, listNokia2g)
        print(listNokia2g)
        #listNokia2g, indexList = funcTestingOutList(listNokia2g, 1)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokia2g": listNokia2g},
        }
    return render(request, "pageNokia2g.html", combined_context)
def funcNokiaTrx(request):
    jsonContents = {}
    listNokiaTrx = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputTrx = request.POST.get("Trx")
        inputNCell = request.POST.get("NCell")
        inputBCXU = request.POST.get("BCXU")
        inputProfile = request.POST.get("Profile")
        inputTrxNumber = request.POST.get("TrxNumber")
        inputTrxFreq = request.POST.get("TrxFreq")
        inputTrx0 = request.POST.get("Trx0")
        inputTrx1 = request.POST.get("Trx1")
        inputTrx2 = request.POST.get("Trx2")
        inputTrx3 = request.POST.get("Trx3")
        inputTrx4 = request.POST.get("Trx4")
        inputTrx5 = request.POST.get("Trx5")
        inputTrx6 = request.POST.get("Trx6")
        inputTrx7 = request.POST.get("Trx7")
        inputReg, inputNumber, listNokiaTrx, inputTrx, inputNCell, inputBCXU, inputProfile, inputTrxNumber, inputTrxFreq, inputTrx0, inputTrx1, inputTrx2, inputTrx3, inputTrx4, inputTrx5, inputTrx6, inputTrx7 = funcNokiaTrxList(inputReg, inputNumber, listNokiaTrx, inputTrx, inputNCell, inputBCXU, inputProfile, inputTrxNumber, inputTrxFreq, inputTrx0, inputTrx1, inputTrx2, inputTrx3, inputTrx4, inputTrx5, inputTrx6, inputTrx7)
        print(listNokiaTrx)
        #listNokiaTrx, indexList = funcTestingOutList(listNokiaTrx, 3)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokiaTrx": listNokiaTrx},
        }
    return render(request, "pageNokiaTrx.html", combined_context)
def funcNokiaSsh(request):
    jsonContents = {}
    listNokiaSsh = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokiaSsh = funcNokiaSshList(inputReg, inputNumber, listNokiaSsh)
        print(listNokiaSsh)
        #listNokiaSsh, indexList = funcTestingOutList(listNokiaSsh, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokiaSsh": listNokiaSsh},
        }
    return render(request, "pageNokiaSsh.html", combined_context)
def funcNokiaHo24(request):
    jsonContents = {}
    listNokiaHo24 = []

    listContents = Content.objects.all()      
    #print(listContents)
    for raw in listContents:
        #print(raw.idmenu)
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokiaHo24 = funcNokiaHo24List(inputReg, inputNumber, listNokiaHo24)
        print(listNokiaHo24)
        #listNokiaHo24, indexList = funcTestingOutList(listNokiaHo24, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokiaHo24": listNokiaHo24},
        }
    return render(request, "pageNokiaho24.html", combined_context)
def funcNokiaPtx3g(request):
    jsonContents = {}
    listNokiaPtx3g = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputPtxCellMax = request.POST.get("PtxCellMax")
        inputReg, inputNumber, listNokiaPtx3g, inputPtxCellMax = funcNokiaPtx3gList(inputReg, inputNumber, listNokiaPtx3g, inputPtxCellMax)
        print(listNokiaPtx3g)
        #listNokiaPtx3g, indexList = funcTestingOutList(listNokiaPtx3g, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokiaPtx3g": listNokiaPtx3g},
        }
    return render(request, "pageNokiaPtx3g.html", combined_context)
def funcNokiaMassLock(request):
    jsonContents = {}
    listNokiaMassLock = []

    listContents = Content.objects.all()      
    #print(listContents)
    for raw in listContents:
        #print(raw.idmenu)
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":        
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputReg, inputNumber, listNokiaMassLock = funcNokiaMassLockList(inputReg, inputNumber, listNokiaMassLock)
        print(listNokiaMassLock)
        #listNokiaMassLock, indexList = funcTestingOutList(listNokiaMassLock, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listNokiaMassLock": listNokiaMassLock},
         }
    return render(request, "pageNokiaMassLock.html", combined_context)
def funcEricssonStart(request):
    jsonContents = {}
    listEricssonStart = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listEricssonStart = funcEricssonStartList(inputReg, inputNumber, inputBB, listEricssonStart)
        print(listEricssonStart)
        #listEricssonStart, indexList = funcTestingOutList(listEricssonStart, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listEricssonStart": listEricssonStart},
        }
    return render(request, "pageEricsssonStart.html", combined_context)
def funcEricsson4g(request):
    jsonContents = {}
    listEricsson4g = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listEricsson4g = funcEricsson4gList(inputReg, inputNumber, inputBB, listEricsson4g)
        print(listEricsson4g)
        #listEricsson4g, indexList = funcTestingOutList(listEricsson4g, 5)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listEricsson4g": listEricsson4g},
        }
    return render(request, "pageEricssson4g.html", combined_context)
def funcEricsson3g(request):
    jsonContents = {}
    listEricsson3g = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listEricsson3g = funcEricsson3gList(inputReg, inputNumber, inputBB, listEricsson3g)
        print(listEricsson3g)
        #listEricsson3g, indexList = funcTestingOutList(listEricsson3g, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listEricsson3g": listEricsson3g},
        }
    return render(request, "pageEricsson3g.html", combined_context)
def funcEricsson3gsix(request):
    jsonContents = {}
    listEricsson3gsix = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listEricsson3gsix = funcEricsson3gsixList(inputReg, inputNumber, inputBB, listEricsson3gsix)
        #listEricsson3gsix, indexList = funcTestingOutList(listEricsson3gsix, 4)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listEricsson3gsix": listEricsson3gsix},
        }
    return render(request, "pageEricsson3gsix.html", combined_context)
def funcEricsson2g(request):
    jsonContents = {}
    listEricsson2g = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listEricsson2g = funcEricsson2gList(inputReg, inputNumber, inputBB, listEricsson2g)
        #listEricsson2g, indexList = funcTestingOutList(listEricsson2g, 5)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listEricsson2g": listEricsson2g},
        }
    return render(request, "pageEricsson2g.html", combined_context)
def funcEricssonLic(request):
    jsonContents = {}
    listMain = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listMain = funcEricssonLicList(inputReg, inputNumber, inputBB, listMain)
        print(listMain)
        #listMain, indexList = funcTestingOutList(listMain, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listMain": listMain},
        }
    return render(request, "pageEricssonLic.html", combined_context)
def funcEricssonRet(request):
    jsonContents = {}
    listMain = []

    listContents = Content.objects.all()      
    for raw in listContents:
        if raw.idmenu not in jsonContents:
            jsonContents[raw.idmenu] = []
        jsonContents[raw.idmenu].append({
            "id": raw.id,
            "title": raw.title,
            "content": raw.content,
            "idcard": raw.idcard,
            "idmenu": raw.idmenu,
            "author": raw.author,
            "date": raw.date
        })

    if request.method == "POST":
        inputReg = request.POST.get("Reg")
        inputNumber = request.POST.get("NS")
        inputBB = request.POST.get("BB")
        inputReg, inputNumber, inputBB, listMain = funcEricssonRetList(inputReg, inputNumber, inputBB, listMain)
        print(listMain)
        #listMain, indexList = funcTestingOutList(listMain, 0)

    combined_context = {
        **{"jsonContents": jsonContents},
        **{"listMain": listMain},
        }
    return render(request, "pageEricssonRet.html", combined_context)