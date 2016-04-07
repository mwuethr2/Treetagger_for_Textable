self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.sendButton.settingsChanged,
        )
        
#donne un attribut à cet objet advancedSettings. le recopier tel quel sur notre code treetagger
        self.advancedSettings.draw()# premier chose qu'on fait après avoir sélectionner advancedSettings, c'est de la dessiner.

#advancedSettings ne cache rien, ca ajoute des variables sur la fenetre. Dans l'espace que suit la case advancedSettings
#        
#
## Filter box (advanced settings only)
        filterBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Filter',
            orientation='vertical',
        )
        filterCriterionCombo = OWGUI.comboBox(
            widget=filterBox,
            master=self,
            value='filterCriterion',
            items=[u'author', u'year', u'genre'],
            sendSelectedValue=True,
            orientation='horizontal',
            label=u'Criterion:',
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        filterCriterionCombo.setMinimumWidth(120)
        OWGUI.separator(widget=filterBox, height=3)
        self.FilterValueCombo = OWGUI.comboBox(
            widget=filterBox,
            master=self,
            value='filterValue',
            orientation='horizontal',
            label=u'Value:',
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        OWGUI.separator(widget=filterBox, height=3)
        
        # The following lines add filterBox (and a vertical separator) to the
        # advanced interface...
        self.advancedSettings.advancedWidgets.append(filterBox)
        self.advancedSettings.advancedWidgetsAppendSeparator() #cree des espaces entre les boxes
        
#
#       def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            
        if len(self.titleLabels) > 0:
            self.selectedTitleLabels = self.selectedTitleLabels
#
