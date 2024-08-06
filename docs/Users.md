# Users management

## Disclamer

Following notes explain some limitations about the usage of the following documentation:

1. Some feature will not be available until the SMTP server is provided and configured.
2. The procedure refers to the 'Server administrator', only the user 'Admin' have this kind of permission.

## User management

The following topics on [Grafana documentation](https://grafana.com/docs/grafana/latest/administration/user-management/) describe how to use permissions to control user access to data sources, dashboards, users, and teams.

- [Server user management](https://grafana.com/docs/grafana/latest/administration/user-management/server-user-management/)
- [Manage user preferences](https://grafana.com/docs/grafana/latest/administration/user-management/user-preferences/)
- [Manage users in an organization](https://grafana.com/docs/grafana/latest/administration/user-management/manage-org-users/)
- [Manage dashboard permissions](https://grafana.com/docs/grafana/latest/administration/user-management/manage-dashboard-permissions/)

### Roles and permissions

Summary of list by user role:

| Permission                     | Organization administrator | Editor | Viewer |
| ------------------------------ | -------------------------- | ------ | ------ |
| View dashboards                | x                          | x      | x      |
| Add, edit, delete dashboards   | x                          | x      |        |
| Add, edit, delete folders      | x                          | x      |        |
| View playlists                 | x                          | x      | x      |
| Add, edit, delete playlists    | x                          | x      |        |
| Create library panels          | x                          | x      |        |
| View annotations               | x                          | x      | x      |
| Add, edit, delete annotations  | x                          | x      |        |
| Access Explore                 | x                          | x      |        |
| Add, edit, delete data sources | x                          |        |        |
| Add and edit users             | x                          |        |        |
| Add and edit teams             | x                          |        |        |
| Change organizations settings  | x                          |        |        |
| Change team settings           | x                          |        |        |
| Configure application plugins  | x                          |        |        |

For more information on roles and permissions, please follow Grafana documentation:
<https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/>

## Team management

Teams allow to cover groups of users. It is recommended to use teams when assigning permission on a dashboard or a folder.

To manage teams please follow Grafana documentation: <https://grafana.com/docs/grafana/latest/administration/team-management/>

## Task shortcut

| Task                                                                                                                                               | Permission needed                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 1. [Add a user](https://grafana.com/docs/grafana/latest/administration/user-management/server-user-management/#add-a-user)                         | Server administrator                                                        |
| 1. [Invite a user](https://grafana.com/docs/grafana/latest/administration/user-management/manage-org-users/#invite-a-user-to-join-an-organization) | Organization administrator <br/> **(SMTP server needed)**                   |
| 2. [Create a Team](https://grafana.com/docs/grafana/latest/administration/team-management/#create-a-team)                                          | Organization administrator permissions <br/> Team administrator permissions |
| 3. [Add a team member](https://grafana.com/docs/grafana/latest/administration/team-management/#add-a-team-member)                                  | Organization administrator permissions                                      |
| 4. [Grant team member permissions](https://grafana.com/docs/grafana/latest/administration/team-management/#grant-team-member-permissions)          | Organization administrator permissions <br/> Team administrator permissions |

## Copy a provisioned dashboard

Provisioned dashboards cannot be edited by a user. Editors or Admin users need to copy the dashboard in a folder with editor role assigned to the user.

Then two choice is available:

1. Click on `save` 💾 button. A dialog open informing that the dashboard can not be edited and shows the `json` to be copied. Once the `json` retrieved, add a new `Dashboards -> Import`, then the `json` can be loaded to initiate the new dashboard.

2. Click on the dashboard `settings` ⚙️, then `Save As...` and select the folder where copy the dashboard.
