import datasource
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from tkinter.simpledialog import askinteger, askstring
from messageWindow import MapDisplay

sbi_numbers = 3
bemp_numbers = 3

class Window(tk.Tk): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Create a menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
    # Create "File" menu
        self.command_menu = tk.Menu(self.menubar,tearoff=0)
        self.command_menu.add_command(label="設定", command=self.menu_setting_click)
        self.command_menu.add_command(label="XXXX")
        self.command_menu.add_separator()
        self.command_menu.add_command(label="離開", command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.command_menu)
    #"Search" menu
        self.command_menu2 = tk.Menu(self.menubar,tearoff=0)
        self.command_menu2.add_command(label="搜尋", command=self.menu_search_click)
        self.menubar.add_cascade(label="Search", menu=self.command_menu2)
#mainFrame
        mainFrame = tk.Frame(self)
        mainFrame.pack(padx=30,pady=(100,50))

###建立top_wrapperFrame=================
        top_wrapperFrame = ttk.Frame(mainFrame)
        top_wrapperFrame.pack(fill=tk.X)

###topFrame_start=================
        topFrame = ttk.LabelFrame(top_wrapperFrame,text="台北市行政區")
        topFrame.pack(side=tk.LEFT)

        length = len(datasource.sarea_list) #長度是14

        self.radioStringVar = tk.StringVar()

        for i in range(length):
            #print(datasource.sarea_list[i])
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame,text=datasource.sarea_list[i],value=datasource.sarea_list[i],variable=self.radioStringVar,command=self.radio_Event).grid(column=cols, row=rows, sticky=tk.W, padx=10, pady=10)

        self.radioStringVar.set("士林區")
        self.area_data= datasource.getInfoFromArea("士林區")
###topFrame_end=================

#logoLabel above top_wrapperFrame=======================================================
        logoImage = Image.open(f'./images/{self.radioStringVar.get()}.jpg')
        resizeImage = logoImage.resize((120,80),Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(self,image=self.logoTkimage)
        logoLabel.place(x=420,y=10)

###sbi_warningFrame_start=================
        self.sbi_warningFrame = ttk.LabelFrame(top_wrapperFrame)
        self.sbi_warningFrame.pack(side=tk.LEFT)

        columns = ('#1','#2','#3')
        self.sbi_tree = ttk.Treeview(self.sbi_warningFrame,columns=columns, show='headings')
        self.sbi_tree.heading('#1',text='站點')
        self.sbi_tree.column("#1",minwidth=0, width=200)
        self.sbi_tree.heading('#2',text='可借')
        self.sbi_tree.column("#2",minwidth=0, width=35)
        self.sbi_tree.heading('#3',text='可還')
        self.sbi_tree.column("#3",minwidth=0, width=35)
        self.sbi_tree.pack(side=tk.LEFT)
        self.sbi_warning_data = datasource.filter_sbi_warning_data(self.area_data,sbi_numbers)

        sbi_sites_numbers = len(self.sbi_warning_data)
        self.sbi_warningFrame.configure(text=f"可借不足站點數{sbi_sites_numbers}")

        for item in self.sbi_warning_data:
            self.sbi_tree.insert('',tk.END,values=[item['sna'][11:],item['sbi'],item['bemp']])
###sbi_warningFrame_end=================

###bemp_warningFrame_start=================
        self.bemp_warningFrame = ttk.LabelFrame(top_wrapperFrame)
        self.bemp_warningFrame.pack(side=tk.LEFT)

        columns = ('#1','#2','#3')
        self.bemp_tree = ttk.Treeview(self.bemp_warningFrame,columns=columns, show='headings')
        self.bemp_tree.heading('#1',text='站點')
        self.bemp_tree.column("#1",minwidth=0, width=200)
        self.bemp_tree.heading('#2',text='可借')
        self.bemp_tree.column("#2",minwidth=0, width=35)
        self.bemp_tree.heading('#3',text='可還')
        self.bemp_tree.column("#3",minwidth=0, width=35)
        self.bemp_tree.pack(side=tk.LEFT)
        self.bemp_warning_data = datasource.filter_bemp_warning_data(self.area_data,bemp_numbers)

        bemp_sites_numbers = len(self.bemp_warning_data)
        self.bemp_warningFrame.configure(text=f"可還不足站點數{bemp_sites_numbers}")

        for item in self.bemp_warning_data:
            self.bemp_tree.insert('',tk.END,values=[item['sna'][11:],item['sbi'],item['bemp']])
###bemp_warningtopFrame_end=================

###建立 Treeview------------------------------------------------
    #display current datetime   
        now = datetime.datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
    #建立bottomFrame for treeview
        self.bottomFrame = ttk.LabelFrame(mainFrame,text=f"士林區-{nowString}")
        self.bottomFrame.pack()

        columns = ('#1','#2','#3','#4','#5','#6','#7')
        self.tree = ttk.Treeview(self.bottomFrame,columns=columns, show='headings')
        self.tree.heading('#1',text='站點')
        self.tree.column("#1",minwidth=0, width=200)
        self.tree.heading('#2',text='時間')
        self.tree.column("#2",minwidth=0, width=150)
        self.tree.heading('#3',text='總車數')
        self.tree.column("#3",minwidth=0, width=50)
        self.tree.heading('#4',text='可借')
        self.tree.column("#4",minwidth=0, width=35)
        self.tree.heading('#5',text='可還')
        self.tree.column("#5",minwidth=0, width=35)
        self.tree.heading('#6',text='地址')
        self.tree.column("#6",minwidth=0, width=250)
        self.tree.heading('#7',text='狀態')
        self.tree.column("#7",minwidth=0, width=35)
        self.tree.pack(side=tk.LEFT)

        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['sna'][11:],item['mday'],item['tot'],item['sbi'],item['bemp'],item['ar'],item['act']],tags=item['sna'])

#self.tree bind event 在treeview點選某列會有self.treeSelected的功能
        self.tree.bind('<<TreeviewSelect>>',self.treeSelected)

#幫treeview加scrollbar------------------------------------------------
        scrollbar = ttk.Scrollbar(self.bottomFrame,command=self.tree.yview) 
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

        sbi_scrollbar = ttk.Scrollbar(self.sbi_warningFrame,command=self.sbi_tree.yview) 
        sbi_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.sbi_tree.config(yscrollcommand=sbi_scrollbar.set)

        bemp_scrollbar = ttk.Scrollbar(self.bemp_warningFrame,command=self.bemp_tree.yview) 
        bemp_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.bemp_tree.config(yscrollcommand=bemp_scrollbar.set)

#設定radiobutton事件
    def radio_Event(self):
    #get current datetime
        now = datetime.datetime.now()
    #display current datetime
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")

        #print(type(self.tree.get_children()))
        #print(self.tree.get_children())
    #clear tree view
        for child in self.tree.get_children():
            self.tree.delete(child)
            #.get_children() returns a collection of all the nodes that are directly connected to the root node
        for child in self.sbi_tree.get_children():
            self.sbi_tree.delete(child)
        for child in self.bemp_tree.get_children():
            self.bemp_tree.delete(child)

        area_name = self.radioStringVar.get()
    # Update the label
        self.bottomFrame.config(text=f"{area_name}-{nowString}")

    # Get all station data from selected area
        self.area_data = datasource.getInfoFromArea(area_name)

    # Filter data with sbi warning number
        self.sbi_warning_data = datasource.filter_sbi_warning_data(self.area_data,sbi_numbers)
        sbi_site_numbers = len(self.sbi_warning_data)
        self.sbi_warningFrame.config(text=f"可借不足站點數:{sbi_site_numbers}")
        #print("sbi:")
        #print(self.sbi_warning_data)
        
    # Filter data with bemp warning number
        self.bemp_warning_data = datasource.filter_bemp_warning_data(self.area_data,bemp_numbers)
        bemp_site_numbers = len(self.bemp_warning_data)
        self.bemp_warningFrame.configure(text=f"可還不足站點數:{bemp_site_numbers}")
        #print("bemp:")
        #print(self.bemp_warning_data)

    #Display data in tree view
        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['sna'][11:],item['mday'],item['tot'],item['sbi'],item['bemp'],item['ar'],item['act']],tags=item['sna'])

        for item in self.sbi_warning_data:
            self.sbi_tree.insert('',tk.END,values=[item['sna'][11:],item['sbi'],item['bemp']])

        for item in self.bemp_warning_data:
            self.bemp_tree.insert('',tk.END,values=[item['sna'][11:],item['sbi'],item['bemp']])

    #更改照片=============================================
        logoImage = Image.open(f'./images/{self.radioStringVar.get()}.jpg')
        resizeImage = logoImage.resize((120,80),Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(self,image=self.logoTkimage)
        logoLabel.place(x=420,y=10)

    #點選treeview傳出資料
    def treeSelected(self,event):
        selectedTree = event.widget #The event is generated when the user selects an item in the treeview widget that triggered the event by accessing the widget attribute of the event object.
        itemTag = selectedTree.selection()[0] # It then uses the selection method of the treeview widget to get the list of tags of the selected items.

        #print(selectedTree.selection()[0]) 得出treeview的編號,[0]是指list裡面的第一個

        itemDic = selectedTree.item(itemTag)
        #print(itemDic)
        siteName = itemDic['tags'][0]
        #print(itemDic['tags']) --> itemDic['tag']是一個list,所以加[0]是取出list裡面的第一個值
        #print(siteName) -->是值，不是list
        for item in self.area_data:
            if siteName == item['sna']:
                selected_data = item
                break #不寫也可以，但因為結果就是只有一筆，寫break才不會跑很多次浪費
#顯示地圖window=================
        mapDisplay = MapDisplay(self,selected_data) #self是傳到class MapDisplay的master, selected_data是data_dict
        
    #設定menubar中的設定按鍵功能
    def menu_setting_click(self):
        global sbi_numbers, bemp_numbers
        retVal = askinteger(f"目前設定不足數量為:{sbi_numbers}","請輸入不足可借可還數量0~5",minvalue=0, maxvalue=5)
        #askinteger is a function from the tkinter module in Python, which is used to display a dialog box with a message and an entry field for the user to enter an integer value. 
        #print(retVal)
        sbi_numbers = retVal
        bemp_numbers = retVal

    # #設定menubar中的搜尋按鍵功能
    def menu_search_click(self):
        site_str = askstring("查詢的站點名","請輸入想查詢的地名關鍵字") 
        for child in self.tree.get_children():
            self.tree.delete(child)
        for item in datasource.data_list:
            if site_str in (item['sna']) or site_str in (item['ar']):
                self.tree.insert('',tk.END,values=[item['sna'][11:],item['mday'],item['tot'],item['sbi'],item['bemp'],item['ar'],item['act']],tags=item['sna'])
                
        

def main():
    #datasource.getInfo()
    #print(datasource.sarea_list)
    window=Window()
    window.title("台北市Ubike2.0即時資訊")
    window.mainloop()


if __name__ == "__main__":
    main()