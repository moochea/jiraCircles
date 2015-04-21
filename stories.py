#!/usr/bin/env python
from jira.client import JIRA
import inspect, re, json
from config import *

def filtered_issues(jira,query):
    issues = jira.search_issues(query, maxResults=100)
    return issues


def fetch_jira_issues(server, username, password, search_filter):
    jira_options = {'server': server}
    jira = JIRA(options=jira_options, basic_auth=(username,password))

    return filtered_issues(jira,search_filter)


        

def populate_stories_stub():
    storyQueue={}

#    story1 = Story("TSM-25",252525, "Chea", 2)
#    story1.move_to(170,410)
#    story1.set_title("This is a bad defect")
#    story1.update_progress(60)
#    storyQueue[story1.key]=story1
#
#    story2 = Story("TSM-26",262626,"Munchy",5)
#    story2.move_to(410,170)
#    story2.set_title("Time machine")
#    story2.set_summary("How to create a time machine with only 5 tools")
#    story2.update_state(0)
#    storyQueue[story2.key]=story2

    story3 = Story("TSM-27",272727,"Adam", 10)
    story3.move_to(200,250)
    story3.update_state(4)
#    story3.set_dependency("TSM-26")
    story3.set_dependency("TSM-35")
    story3.set_summary("This story will never get done")
    story3.set_title("Never done")
    storyQueue[story3.key]=story3

    story4 = Story("TSM-35",53535,"Adam", 3)
    story4.move_to(400,250)
    story4.update_state(5)
    story4.set_title("run and hide")
    story4.set_summary("Sometimes I run, sometimes I hide")
#    story4.set_dependency(26)
    storyQueue[story4.key]=story4

    return storyQueue

def populate_stories_jira(login, password, server, story_filter):
    #print login, password, server, story_filter
    storyQueue = {}
#    filters={
#            "master 32" : "project = TSM AND sprint = 402 and type != 'Technical task'",
#            "master 31" : "project = TSM AND sprint = 391",
#            "master 33" : "project = TSM AND sprint = 405 and type != 'Technical task'",
#            }

#    server='http://jira.vsl.com.au'
    username = login
#    password = "password"
    

#    issues = fetch_jira_issues(server, username, password, filters["master 32"])
    issues = fetch_jira_issues(server, login, password, story_filter)

    #figuring out where to position them
    spread = math.ceil(math.sqrt(len(issues)))
    pozx = WINDOW_WIDTH/spread
    pozy = WINDOW_HEIGHT/spread
    px=20
    py=20
    for x in issues:
        key = x.key
        assignee = x.fields.assignee
        summary = x.fields.summary
        status = x.fields.status.name
##        project = x.fields.project
        storyId = x.id
        storyPoints=1
        try:
            points= x.fields.customfield_10232
            if points !=None:
                if int(points)>0:
                    storyPoints = int(points)
                else:
                    storyPoints=1
        except AttributeError:
            storyPoints=1

        storyQueue[key] = Story(key,storyId, assignee,storyPoints)
        storyQueue[key].set_summary(summary)
#        storyQueue[key].set_title(summary)

#
        px=px+pozx
        if px >= WINDOW_WIDTH-20:
            px=pozx
            py=py+pozy
        if py>=WINDOW_HEIGHT-20:
            py=pozy
#
        storyQueue[key].move_to(int(px),int(py))
#            if status == "Complete":
#            elif status == "Awaiting Verification":
#            elif status == 

        if status == "Awaiting Verification":
            storyQueue[key].update_state(2)
        elif status == "In Progress":
            storyQueue[key].update_state(1)
        elif status == "Complete": 
            storyQueue[key].update_state(3)
        elif status == "Rejected": 
            storyQueue[key].update_state(6)
        else:
           pass
        #print key, storyPoints, summary, px, py
    return storyQueue

def file_output(storyQueue, filename):
    stories = {}

    for x in storyQueue:
        stories[x] = {}
        for y in dir(storyQueue[x]):
            if re.search("__",y) == None:
                val=getattr(storyQueue[x],y)
                if not inspect.ismethod(val):
#                    print y,": ", val
                    if (y=="assigned" and not isinstance(val, str) and not isinstance(val, unicode)):
                        #print y, val, type(val)
                        if val:
                            stories[x][y] = val.displayName
                        else:
                            stories[x][y] = None
                    else:
                        stories[x][y] = val
#        print "\n"

    #print stories
    newline = json.dumps(stories,indent=4 )
#    print newline

    newfile = open(filename,"w")
    newfile.write(newline)
    newfile.close()

def load_objects(filename):
    filename = open(filename, "r")
    newline = filename.read()
    filename.close()
    stories_dict = json.loads(newline)
    
    return stories_dict
            
def load_stories_from_dict(story_dict):
    stories={}
    for x in story_dict:
#    newariey = Story(**story_dict)
        newstory = Story(story_dict[x]["key"],story_dict[x]["storyId"],story_dict[x]["assigned"],story_dict[x]["storyPoints"])
        newstory.update_progress(story_dict[x]["progress"])
        newstory.update_state(story_dict[x]["state"])
        newstory.set_title(story_dict[x]["title"])
        newstory.set_summary(story_dict[x]["summary"])
        for dd in story_dict[x]["dependencies"]:
            newstory.set_dependency(dd)
        newstory.move_to(story_dict[x]["xCoord"], story_dict[x]["yCoord"])
        stories[(story_dict[x]["key"])]=newstory
    return stories

class Story:
    def __init__(self, key,storyId, assigned, storyPoints=2):
        self.key = key
#        self.project = project
        self.assigned=assigned
        self.storyPoints=storyPoints
        self.dependencies = []
        self.progress = 0
        self.state = 0
        self.storyId=storyId
        self.xCoord = WINDOW_X
        self.yCoord = WINDOW_Y
        self.title =  " " 
#        self.display=True
        self.summary="summary"

    def move_to(self,x,y):
        self.xCoord = x
        self.yCoord = y
#        print "circle coords: ", x,y

    def set_title(self, title):
        self.title = title

    def update_progress(self, new_prog):
        self.progress = new_prog
        if self.progress > 0 and self.state == 0:
            self.state = 1
        elif self.progress == 100 and self.state in (0,1,4):
            self.state = 3
        elif self.progress < 100 and self.state == 3:
            self.state = 2

    def update_state(self, new_state):
        self.state = new_state
        if story_states[self.state] in state_progress:
            self.progress = state_progress[story_states[self.state]]
#        if self.state == 3:
#            self.progress = 100
#        elif self.state == 0:
#            self.progress = 0
#        elif self.state == 2:
#            self.progress = 75

    def set_dependency(self, dependency):
        self.dependencies.append(dependency)

    def remove_dependency(self, dependency):
        if dependency in self.dependencies:
           self.dependencies.remove(dependency)
        
    def set_summary(self, summary):
        self.summary = summary

    def set_display(self, newdisplay):
        self.display=newdisplay

if __name__ == "__main__":   
  
    story_parts = ["key","summary","assigned", "state","progress"]
#    storyQueue = populate_stories_stub()

#    file_output(storyQueue, "newfile")

    
    stories = load_objects("newfile")
#    for x in stories:
        #print stories[x]
#        for y in stories[x]:
            #print y, ": ", stories[x][y]
