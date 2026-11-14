import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class SchoolDashboard extends Component {
    static template = "openeducat_dashboard.SchoolDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ loading: true, error: false, data: null });
        this.strings = {
            loading: "جارٍ تحميل ملخص المدرسة...",
            welcome: "مرحباً بعودتك",
            subtitle: "نظرة سريعة وشاملة على سير العمليات التعليمية والمدرسية اليوم.",
            overview: "ملخص المدرسة",
            viewDetails: "عرض التفاصيل",
            quickAccess: "الوصول السريع",
            retry: "إعادة المحاولة",
        };
        this.metrics = [
            {
                key: "students",
                label: "الطلاب المنتظمون",
                icon: "fa-graduation-cap",
            },
            {
                key: "admissions",
                label: "طلبات القبول قيد الإجراء",
                icon: "fa-file-text-o",
            },
            {
                key: "attendance",
                label: "جلسات الحضور والغياب اليوم",
                icon: "fa-calendar-check-o",
            },
            {
                key: "courses",
                label: "المراحل والصفوف النشطة",
                icon: "fa-book",
            },
        ];
        this.shortcuts = [
            { key: "students", label: "سجل الطلاب", icon: "fa-users" },
            { key: "admissions", label: "إدارة القبول", icon: "fa-inbox" },
            { key: "attendance", label: "سجل الحضور", icon: "fa-calendar" },
            { key: "courses", label: "المراحل والمقررات", icon: "fa-book" },
        ];
        onWillStart(() => this.loadDashboard());
    }

    async loadDashboard() {
        this.state.loading = true;
        this.state.error = false;
        try {
            this.state.data = await this.orm.call(
                "openeducat.dashboard",
                "get_dashboard_data",
                [],
            );
        } catch (error) {
            console.error("Could not load the OpenEduCat dashboard.", error);
            this.state.error = "تعذر تحميل لوحة التحكم. يرجى التحقق من الصلاحيات والمحاولة مجدداً.";
        } finally {
            this.state.loading = false;
        }
    }

    openAction(actionId) {
        return this.action.doAction(actionId);
    }
}

registry.category("actions").add("openeducat_school_dashboard", SchoolDashboard);
