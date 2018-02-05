#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

from AnyQt.QtGui import QStandardItem, QStandardItemModel

class TreeItem(QStandardItem):
    
    def __init__(self, obj, parent=None):
        super(TreeItem, self).__init__(obj.name)


class TreeModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__()
        self._objects = {}

        self.itemChanged.connect(self.__itemChanged)
        self.rowsInserted.connect(self.__rowsInserted)

    def __rowsInserted(self, parent, start, end):
        #print self.itemFromIndex(parent)
        pass
      
    def __itemChanged(self, item):
        #item._sceneobject = self._objects[item.text()]
        pass

    def nodeChildrens(self, startnode=None, findNode=None):
        if startnode==None: 
            node = self.invisibleRootItem()
        else: 
            node = startnode

        for i in range(node.rowCount()):
            childNode = node.child(i)

            label = str(childNode.text())
            obj = self._objects[label]

            if obj==findNode: return self.getChildrens(childNode, [])

            nodes = self.getNodes(childNode)
            if nodes!=None: return nodes            
        
        return None



    def getNodes(self, startnode=None, findNode=None):
        if startnode==None: node = self.invisibleRootItem()
        else: node = startnode

        res = []
        for i in range(node.rowCount()):
            n = node.child(i)

            label = str(n.text())
            obj = self._objects[label]

            nodes = self.getNodes(n)

            if obj==findNode: return nodes
            if isinstance(nodes, list) and len(nodes)>0: res.append( nodes )
            else: res.append( nodes )

        if startnode==None: return res
        else: 
            if len(res)==0: return node
            else: return (node, res)

    def getChildrens(self, startnode=None, res=[]):
        if startnode==None: 
            node = self.invisibleRootItem()
            res=[]
        else: node = startnode

        for i in range(node.rowCount()):
            n = node.child(i)
            key = str(n.text())
            if key in self._objects:
                res.append(self._objects[key])
            self.getChildrens(n, res)

        return res