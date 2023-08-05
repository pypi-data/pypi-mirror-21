// This file is auto generated, the git version is blank and .gitignored
export const pluginRoutes = [
    {
        path: 'peek_plugin_active_task',
        loadChildren: "peek_plugin_active_task/plugin-active-task.module#PluginActiveTaskAdminModule"
    },
    {
        path: 'peek_plugin_chat',
        loadChildren: "peek_plugin_chat/chat.module#ChatModule"
    },
    {
        path: 'peek_plugin_noop',
        loadChildren: "peek_plugin_noop/noop.module#NoopModule"
    },
    {
        path: 'peek_plugin_pof_event',
        loadChildren: "peek_plugin_pof_event/pof.events.module#PofEventModule"
    },
    {
        path: 'peek_plugin_pof_field_switching',
        loadChildren: "peek_plugin_pof_field_switching/plugin-pof-field-switching.module#PluginPofFieldSwitchingAdminModule"
    },
    {
        path: 'peek_plugin_pof_soap',
        loadChildren: "peek_plugin_pof_soap/plugin-pof-soap.module"
    },
    {
        path: 'peek_plugin_pof_sql',
        loadChildren: "peek_plugin_pof_sql/plugin-pof-sql.module"
    },
    {
        path: 'peek_plugin_user',
        loadChildren: "peek_plugin_user/plugin-user.module#PluginUserDbAdminModule"
    }
];
