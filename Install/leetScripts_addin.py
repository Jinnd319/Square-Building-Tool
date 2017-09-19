import arcpy
import pythonaddins
import os
import math
import sys
import getpass

#Author: Jack Wilson
class setCenterpoint(object):
    """Implementation for leetScripts_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.cursor = 3
        
#selects a point on the map
    def onMouseDownMap(self, x, y, button, shift):
        print "onMouseDowMap executing"
        setCenterpoint.enabled = True 
        self.x = x
        self.y = y       
        print "Selected point is at %r, %r" % (self.x, self.y)
        print __name__
        pass

    
class setArea(object):
    """Implementation for leetScripts_addin.combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        #self.dropdownWidth = ''
        self.width = 'WWWWWWWWW'
        
#Takes user input Area and returns half the side length of the square
    def onEditChange(self,text) :
        squareFeet = text 
        self.buffDist = (math.sqrt(float(squareFeet))/2)
        print "Square size: %r ft^2 Buffer Distance: %r ft^2" % (squareFeet,
                                                                 self.buffDist)
        print __name__

        return self.buffDist
        pass


#returns workspace, feature dataset, featureclass, instance,
#and database if availible by clicking after the feature class is
#selected in the catalog window.
class SetLayer(object):
    """Implementation for leetScripts_addin.button2 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        
    def onClick(self):
        self.a = pythonaddins.GetSelectedCatalogWindowPath()
        self.a = self.a.encode('mbcs')
        print self.a
        self.b = os.path.split((self.a))
        self.c = self.b[0]
        self.d = os.path.split(self.c)
        self.featureClass = (self.b[1])
        self.featureDataset = (self.d[1])
        self.versionWorkspace = (self.d[0])
        self.workspaceHeadTail = os.path.split(self.versionWorkspace)
        self.workspaceTail = self.workspaceHeadTail[1]
        self.workspaceHead = self.workspaceHeadTail[0]
        self.previousWorkspace = self.workspaceHead + r"/" + self.workspaceTail
        print "Feature class: %r" % self.featureClass
        print "Feature dataset: %r" % self.featureDataset
        print "Workspace: %r" % self.previousWorkspace
        fc = os.path.join(self.versionWorkspace, self.featureDataset,
                          self.featureClass)
        desc = arcpy.Describe(fc)
        print "%r" % desc
        #returns value if sde
        sde = desc.catalogPath.find('.sde')
        #self.isSDE returns False if data is not version and True if it
        #is
        self.isSDE = False
        if sde != -1 and desc.isVersioned:
            self.isSDE = True
            connProp = arcpy.Describe(self.versionWorkspace).connectionProperties
            self.h = connProp.instance.split(":", 2)
            self.instanceX = self.h[2].encode('mbcs')
            self.databaseX = connProp.database.encode('mbcs')
            print "Instance is %r" % self.instanceX
            print "Database is %r" % self.databaseX
            self.List = arcpy.da.ListVersions(self.versionWorkspace)
            self.nameList = []
            for version in self.List:
                self.nameList.append(version.name)
            #getpass.getuser() gets the user computer username and then
            #searchs for right version from list by searching for the
            #string that contains the user computer username. This
            #means that this will need to be changed in user username is
            #not in version name
            found = False
            position = 0
            employeeID = getpass.getuser()

            #Searches for user version. Will grab first version in list
            #with user's computer username.
            self.versionList = []
            while position < len(self.nameList) and not found:
                if str(self.nameList[position]).find(employeeID) != -1:
                    found = True
                    self.currentVersion = self.nameList[position]
                    
                if position == (len(self.nameList)- 1) and not found:
                    print "Employee number not in any versions."
                position += 1
            print "Version is %r" % self.currentVersion   
        print "Tool finished"
        pass


#Draws building and puts it in map    
class buildingTool(object):
    """Implementation for leetScripts_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        print "building tool button is executing"
    #Variables for Creating the polygon
        xCoordinate = float(tool.x)
        yCoordinate = float(tool.y)
        #I'll fix this variable name later. My bad.
        #bob is the buffer distance
        bob = float(combobox.buffDist)

        print "Centroid of buidling:(%r,%r) Side length: %r" % (xCoordinate,
                                                                yCoordinate,
                                                                bob)
        print __name__
        
        def doStuff():
            #Calculates and creates an array of vertex points, opens an
            #insert cursor, creates a polygon using the arra, and inserts
            #building into the appropriate database.
            vertices = []
            vertices.append(arcpy.Point((xCoordinate + bob), (yCoordinate + bob)))
            vertices.append(arcpy.Point((xCoordinate + bob), (yCoordinate - bob)))
            vertices.append(arcpy.Point((xCoordinate - bob), (yCoordinate - bob)))
            vertices.append(arcpy.Point((xCoordinate - bob), (yCoordinate + bob)))
            vertices.append(arcpy.Point((xCoordinate + bob), (yCoordinate + bob)))

            cursor = arcpy.da.InsertCursor( fc, ["SHAPE@"])
            array = arcpy.Array(vertices)
            simpleBuilding = arcpy.Polygon(array)
            cursor.insertRow([simpleBuilding])
            
            del cursor
            print "Building should be drawn"

            
        def makeConnection(authenticationType, pathParent):
            #Creates connection file so code can edit .sde database
            #make this work when r"U:\tempstuff" already exists
            outFolderPath = pathParent
            outName = r"actualName" + str(button2.databaseX) + r".sde"
            databasePlatform = "SQL_Server"
            instance = button2.instanceX
            database = button2.databaseX
            username = "username"#doesn't seem to matter
            password = "password"#doesn't seem to matter
            version = button2.currentVersion
            
            arcpy.CreateDatabaseConnection_management(outFolderPath,
                                                        outName,
                                                        databasePlatform,
                                                        instance,
                                                        authenticationType,
                                                        username, password,
                                                        'DO_NOT_SAVE_USERNAME',
                                                        database,
                                                        '','TRANSACTIONAL',
                                                        version,'')

        fcName = button2.featureClass
        workspace = button2.versionWorkspace
        featureDataset = button2.featureDataset
        fc = os.path.join(workspace, featureDataset, fcName)

#Action to take if layer is in a .sde version.
        if button2.isSDE == True:
            
            database = str(button2.databaseX)
            pathParent = r"U:\tempBuildingTool"
            path = pathParent + r"\actualName" + database + r".sde"
            
            if not os.path.isdir(r"U:\tempBuildingTool"):
                os.makedirs(pathParent)

                
            if not os.path.isfile(path):
                authenticationType = 'OPERATING_SYSTEM_AUTH'
                makeConnection(authenticationType, pathParent)

                
            workspace = pathParent + r"\actualName"  + database + r".sde"
            fc = os.path.join(workspace, featureDataset, fcName) 
            print workspace
            print "Feature class is %r" % fc
            print "initiating editing"
            
    #Catching all errors with the table view or using the same trick 
    #with isSDE to make sure table view is only created when it needs
    #to be.
    
    #Occassionally there is a strange error that appears because the
    #the connection file is too old. If you're getting an error 
    #regarding the tableview or if the building isn't being drawn and
    #even though you're not getting an error, try deleting the
    #connection file. The script will rebuild it for you. 
            if not arcpy.Exists("editView" + database):  
                try:
                #occasionally fails because the connection file is too
                #old. Just delete the connecton file and a new one will
                #be made next time you run the tool
                    tableView = arcpy.MakeTableView_management(fc,
                                                "editView" + database,
                                               "",workspace,
                                               '')
                    button2.isTableView = True
                except arcpy.ExecuteError:
                    pass

                arcpy.ChangeVersion_management((tableView),"TRANSACTIONAL",
                                                       button2.currentVersion,
                                                       '')
  
            try:
                edit = arcpy.da.Editor(workspace)
                edit.startEditing(True, True)
                edit.startOperation()

                doStuff()
                print "made it past function call."
                edit.stopOperation()
                print "Stopping editing"
                edit.stopEditing(True)
            except RuntimeError:
                print "Still in an edit session"

        #if no versions then the function runs without using the
        #connection file    
        else:
            print "made it to else statemenet"
            fc = button2.featureClass
            doStuff()
            print "made it past function call"
        
