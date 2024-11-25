

frappe.ui.form.on('Quotation', {
    refresh(frm) {
    frm.add_custom_button(__("Sales Order."), function(){
            
                frappe.model.open_mapped_doc({
                    method: "erpnext.selling.doctype.quotation.quotation.make_sales_order",
                    frm: frm,
                });
        }, __("Create"));         

    }
})
