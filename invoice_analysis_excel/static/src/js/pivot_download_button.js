/** @odoo-module **/

import { PivotRenderer } from "@web/views/pivot/pivot_renderer";
import { download } from "@web/core/network/download";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PivotRenderer.prototype, {
    downloadCustomExcel() {
        if (this.model.getTableWidth() > 16384) {
            throw new Error(
                _t(
                    "For Excel compatibility, data cannot be exported if there are more than 16384 columns.\n\nTip: try to flip axis, filter further or reduce the number of measures."
                )
            );
        }
        const table = this.model.exportData();
        const searchParams = this.model.searchParams;
        const data = {
            table: table,
            domain: searchParams.domain,
            context: searchParams.context,
        };
        download({
            url: "/invoice_analysis_excel/export_xlsx",
            data: { data: new Blob([JSON.stringify(data)], { type: "application/json" }) },
        });
    }
});