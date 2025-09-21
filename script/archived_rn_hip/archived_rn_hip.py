import archived_rn_hip_ui
from archived_rn_hip_model import ArchivedModel


class ArchivedHip:
    def __init__(self):
        self.ui = archived_rn_hip_ui.ArchivedUI()
        self.model = ArchivedModel()

        self.ui.select_btn_func(lambda: self._select_geo())
        self.ui.whole_chk_func(lambda state: self.whole_check(state))
        self.ui.rn_func(lambda: self.rn_info())
        self.ui.close_ui(lambda: self.ui.close())


    def _select_geo(self):
        geo_tree_dlg = archived_rn_hip_ui.GeoTreeDialog(parent=self.ui)
        geo_tree_dlg.selectSignal.connect(self.geo_tree_handle_select)
        geo_tree_dlg.closeSignal.connect(self.geo_tree_handle_cancel)
        geo_tree_dlg.exec_()


    def geo_tree_handle_select(self, node):
        if node.path() == '/obj':
            self.ui.message_box('error', 'Select Error', 'Selected geometry Node')
            return
        self._set_init_cache_wg(node)


    def _set_init_cache_wg(self, node):
        cache_tbl = self.ui.table_wg
        column_count = cache_tbl.columnCount()

        cache_tbl.setRowCount(0)
        self.model.node_list = []
        current_row_count = cache_tbl.rowCount()

        tmp_tbl_list = []

        wish_nodes = []
        for child in node.children():
            t = child.type()
            if t.category().name() == 'Sop' and\
                  t.name() in ["filecache::2.0", "alembic", "file", "usdimport"]:
                wish_nodes.append(child)
        
        if not wish_nodes:
            self.ui.message_box('error', 'Node Empty', 
                                '["cache", "alembic", "file", "usd"] is not exists')
            return
        
        new_rows_count = len(wish_nodes)
        cache_tbl.setRowCount(current_row_count + new_rows_count)

        for idx, select_node in enumerate(wish_nodes):
            row_idx = current_row_count + idx
            wg_list = []

            for col_idx in range(column_count):
                if col_idx == 0:
                    chkbox_item = archived_rn_hip_ui.CheckBoxWidget()
                    chkbox_item.chk_box.setCheckable(True)
                    chkbox_item.chk_box.setChecked(True)
                    cache_tbl.setCellWidget(row_idx, col_idx, chkbox_item)
                    wg_list.append(chkbox_item.chk_box)
                
                elif col_idx == 1:
                    lb_item = archived_rn_hip_ui.LabelWidget()
                    node_name = select_node.name()
                    lb_item.lb.setText(node_name)
                    cache_tbl.setCellWidget(row_idx, col_idx, lb_item)
                    wg_list.append(select_node)

                elif col_idx == 2:
                    edt_item = archived_rn_hip_ui.LineEditWidget()

                    if select_node.type().name() == "filecache::2.0":
                        dir_path = select_node.parm('basedir').rawValue()
                        edt_item.line_edt.setText(dir_path)
                    
                    elif select_node.type().name() == "alembic":
                        abc_path = select_node.parm('fileName').rawValue()
                        edt_item.line_edt.setText(abc_path)
                    
                    elif select_node.type().name() == "file":
                        file_path = select_node.parm('file').rawValue()
                        edt_item.line_edt.setText(file_path)
                    
                    elif select_node.type().name() == "usdimport":
                        usd_path = select_node.parm('filepath1').rawValue()
                        edt_item.line_edt.setText(usd_path)

                    cache_tbl.setCellWidget(row_idx, col_idx, edt_item)
                    wg_list.append(edt_item.line_edt)

            tmp_tbl_list.append(wg_list)

        select_node_path = str(node.path())
        self.ui.select_edt.setText(select_node_path)
        self.ui.whole_check.setChecked(True)

        self.model.select_geo = str(select_node_path)
        self.model.node_list = tmp_tbl_list


    def geo_tree_handle_cancel(self):
        print('Geo tree close')
        return


    def whole_check(self, state):
        if self.model.node_list:
            for chk, _, _ in self.model.node_list:
                chk.setChecked(state)
        else:
            self.ui.message_box('error', 'Node Empty(1)', 'Select geo Node plz')
            return 


    def rn_info(self):
        if not self.model.node_list:
            self.ui.message_box('error', 'Node Empty(2)', 'Select geo Node plz')
            return
        
        src_txt = self.ui.rn_src_edt.text()
        tr_txt = self.ui.rn_tr_edt.text()

        if not src_txt:
            self.ui.message_box('error', 'Src Empty', 'Write the Src Info')
            return 
        
        if not tr_txt:
            self.ui.message_box('error', 'Tr Empty', 'Write the Target Info')
            return
        
        if src_txt == tr_txt:
            self.ui.message_box('error', 'Same Rename Info', 'Write the Different Src and Target Info.')
            return

        if True not in [chk.isChecked() for chk, _, _ in self.model.node_list]:
            self.ui.message_box('error', 'None Check', 'Check the Convert Node Path')
            return

        if not any(src_txt in str(path.text()) for _, _, path in self.model.node_list):
            self.ui.message_box('error', 'Src Not Found',
                                'The Src Info is not contained in any BasePath.')
            return

        for chk, node, path in self.model.node_list:
            if chk.isChecked():
                if src_txt in str(path.text()):
                    path_txt = str(path.text())
                    path_txt = path_txt.replace(src_txt, tr_txt)

                    if node.type().name() == "filecache::2.0":
                        node.parm('basedir').set(str(path_txt))

                    elif node.type().name() == "alembic":
                        node.parm('fileName').set(str(path_txt))

                    elif node.type().name() == "file":
                        node.parm('file').set(str(path_txt))
                    
                    elif node.type().name() == "usdimport":
                        node.parm('filepath1').set(str(path_txt))
                    
                    path.setText(path_txt)
        
        self.ui.rn_src_edt.setText('')
        self.ui.rn_tr_edt.setText('')
        self.ui.message_box('info', 'Convert Job', 'Done')

