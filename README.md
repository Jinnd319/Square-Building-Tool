#Square Building Tool Readme

	This is a tool that creates square buildings of any size made with python add in.
	It was develeoped to work in a SQL Server .SDE database or a File GDB. It should 
	work for you as is assuming that your versions have the username used to log on to
	your computer in them, and you're trying to draw square buildings in an SQL Server
	.SDE database. 
	
	I've included the code with some comments along with the Esri AddIn File. This 
	should be enough for someone to make any changes to my tool that they find 
	necessary. Just double click on the makeaddin script to make your code a tool it
	should still be working. If it's not then just remake the file using python addins
	Feel free to conact me if you need help or if you have any questions or ideas.
	
	How the toolbar works:
		1. Select the layer you want to draw the square building on in the catalog window
		and then click on the blue penguin. This will set the tool to draw buildings in
		the selected layer. You only have to do this when you start drawing buildings in 
		a layer. It should be the leftmost button.
		2. Click on the "Set Centerpoint" button and then click down on the map where you
		want the centerpoint of your square building to be.
		3. Enter the area you want the square building to be drawn with in the "Set Area"
		combobox.
		4. Click doge. It should be the rightmost button. This will draw your building.
		5. Refresh the veiw to see your building. Your building should be drawn if there
		aren't any errors. Send me an email if there are no errors, your building isn't
		drawn, and you've refreshed your view.
		
		Tip: You can see what the toolbar is doing by opening the python window in arcmap
		and monitoring it's output.