/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { titleService } from "@web/core/browser/title_service";

patch(titleService, {
    start() {
        const result = super.start(...arguments);
        result.setParts({ zsmartedu: "SmartEdu | سمارت إديو" });
        return result;
    },
});
