# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 09:21:31 2018

@author: zerow
"""
import datetime
class WebNode:
    def __init__(self, WebPage, Time):
        """ Initialize class """
        self.WebPage = WebPage
        self.Time = Time
        self.pNext = None
        
class WebList:
    def __init__(self):
        """ Initialize linked list """
        self.length = 0
        self.head = None
        
    def IsEmpty(self):
        """ Check if linked list is empty """
        return self.length == 0
    
    def Clear(self):
        """ Clear the whole linked list """
        self.head = None
        self.length = 0
        print("Clear the linked list finished.")
    
    def Append(self, NewWebNode):
        """ Append the web node to the last """
        if isinstance(NewWebNode, WebNode):
            pass
        else:
            print ('Input node is not valid')
            print (exit)
        # Deal with empty list
        if self.IsEmpty():
            self.head = NewWebNode
        else:
            node = self.head
            while node.pNext:
                node = node.pNext
            node.pNext = NewWebNode
        self.length += 1
    
    def Insert(self, WebPage, Time, Index):
        """ Insert a node into the list """
        # First judge if the insertion position is valid
        if type(Index) is int:
            if Index > self.length:
                print("Input index value is out of range.")
                return
            else:
                NewWebNode = WebNode(WebPage, Time)
                CurrentNode = self.head
            # Deal with index
            if Index == 0:
                self.head = NewWebNode
                NewWebNode.pNext = CurrentNode
            else:
                # Locate the node attached to the index
                while Index - 1:
                    CurrentNode = CurrentNode.pNext
                    Index -= 1 
            # Insert the new node
            NewWebNode.pNext = CurrentNode.pNext
            CurrentNode.pNext = NewWebNode
            self.length += 1
            return
        else:
            print ("Input index value is invalid.")
    
    def Delete(self, Index):
        """ Delete the element of certain index position """
        if type(Index) is int:
            if Index > self.length:
                print ("Input index value is out of range.")
                return 
            else:
                CurrentNode = self.head
                if Index == 0:
                    self.head = self.head.pNext
                else:
                    while Index - 1:
                        CurrentNode = CurrentNode.pNext
                        Index -= 1
                    CurrentNode.pNext = CurrentNode.pNext.pNext
                    self.length -= 1
                    return
        else:
            print ("Input index value is invalid.")
            
    def GetWebPage(self, Index):
        """ Extract the web page stored in the position """ 
        if type(Index) is int:
            if Index > self.length:
                print ("Input index value is out of range.")
                return 
            else:
                CurrentNode = self.head
                if Index == 0:
                    return [self.head.WebPage, self.head.Time]
                else:
                    while Index - 1:
                        CurrentNode = CurrentNode.pNext
                        Index -= 1
                    return [CurrentNode.pNext.WebPage, CurrentNode.pNext.Time]
        else:
            print ("Input index value is invalid.")
    
    def GetLength(self):
        """ Return the length of the linked list """
        CurrentNode = self.head
        if CurrentNode:
            i = 1
            while CurrentNode.pNext:
                CurrentNode = CurrentNode.pNext
                i += 1
            return i
        else:
            return 0
    
    def PrintLinkedList(self):
        """ Print all the elements in the linked list """
        if self.IsEmpty():
            print ("The web list is empty.")
        else:
            CurrentNode = self.head
            print (CurrentNode.WebPage)
            while CurrentNode.pNext:
                CurrentNode = CurrentNode.pNext
                print (CurrentNode.WebPage)

if __name__ == '__main__':
    ### Main ###
    print ('Completed construction of linked list.')   
