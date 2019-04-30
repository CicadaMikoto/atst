from atst.models import CSPRole
from atst.utils.localization import translate, translate_duration


SERVICE_BRANCHES = [
    ("", "- Select -"),
    ("Air Force, Department of the", "Air Force, Department of the"),
    ("Army and Air Force Exchange Service", "Army and Air Force Exchange Service"),
    ("Army, Department of the", "Army, Department of the"),
    (
        "Defense Advanced Research Applications Agency",
        "Defense Advanced Research Applications Agency",
    ),
    ("Defense Commissary Agency", "Defense Commissary Agency"),
    ("Defense Contract Audit Agency", "Defense Contract Audit Agency"),
    ("Defense Contract Management Agency", "Defense Contract Management Agency"),
    ("Defense Finance & Accounting Service", "Defense Finance & Accounting Service"),
    ("Defense Health Agency", "Defense Health Agency"),
    ("Defense Information System Agency", "Defense Information System Agency"),
    ("Defense Intelligence Agency", "Defense Intelligence Agency"),
    ("Defense Legal Services Agency", "Defense Legal Services Agency"),
    ("Defense Logistics Agency", "Defense Logistics Agency"),
    ("Defense Media Activity", "Defense Media Activity"),
    ("Defense Micro Electronics Activity", "Defense Micro Electronics Activity"),
    ("Defense POW-MIA Accounting Agency", "Defense POW-MIA Accounting Agency"),
    ("Defense Security Cooperation Agency", "Defense Security Cooperation Agency"),
    ("Defense Security Service", "Defense Security Service"),
    ("Defense Technical Information Center", "Defense Technical Information Center"),
    (
        "Defense Technology Security Administration",
        "Defense Technology Security Administration",
    ),
    ("Defense Threat Reduction Agency", "Defense Threat Reduction Agency"),
    ("DoD Education Activity", "DoD Education Activity"),
    ("DoD Human Recourses Activity", "DoD Human Recourses Activity"),
    ("DoD Inspector General", "DoD Inspector General"),
    ("DoD Test Resource Management Center", "DoD Test Resource Management Center"),
    (
        "Headquarters Defense Human Resource Activity ",
        "Headquarters Defense Human Resource Activity ",
    ),
    ("Joint Staff", "Joint Staff"),
    ("Missile Defense Agency", "Missile Defense Agency"),
    ("National Defense University", "National Defense University"),
    (
        "National Geospatial Intelligence Agency (NGA)",
        "National Geospatial Intelligence Agency (NGA)",
    ),
    (
        "National Oceanic and Atmospheric Administration (NOAA)",
        "National Oceanic and Atmospheric Administration (NOAA)",
    ),
    ("National Reconnaissance Office", "National Reconnaissance Office"),
    ("National Reconnaissance Office (NRO)", "National Reconnaissance Office (NRO)"),
    ("National Security Agency (NSA)", "National Security Agency (NSA)"),
    (
        "National Security Agency-Central Security Service",
        "National Security Agency-Central Security Service",
    ),
    ("Navy, Department of the", "Navy, Department of the"),
    ("Office of Economic Adjustment", "Office of Economic Adjustment"),
    ("Office of the Secretary of Defense", "Office of the Secretary of Defense"),
    ("Pentagon Force Protection Agency", "Pentagon Force Protection Agency"),
    (
        "Uniform Services University of the Health Sciences",
        "Uniform Services University of the Health Sciences",
    ),
    ("US Cyber Command (USCYBERCOM)", "US Cyber Command (USCYBERCOM)"),
    (
        "US Special Operations Command (USSOCOM)",
        "US Special Operations Command (USSOCOM)",
    ),
    ("US Strategic Command (USSTRATCOM)", "US Strategic Command (USSTRATCOM)"),
    (
        "US Transportation Command (USTRANSCOM)",
        "US Transportation Command (USTRANSCOM)",
    ),
    ("Washington Headquarters Services", "Washington Headquarters Services"),
]

ASSISTANCE_ORG_TYPES = [
    ("In-house staff", "In-house staff"),
    ("Contractor", "Contractor"),
    ("Other DoD Organization", "Other DoD Organization"),
    ("None", "None"),
]

DATA_TRANSFER_AMOUNTS = [
    ("", "Select an option"),
    ("Less than 100GB", "Less than 100GB"),
    ("100GB-500GB", "100GB-500GB"),
    ("500GB-1TB", "500GB-1TB"),
    ("1TB-50TB", "1TB-50TB"),
    ("50TB-100TB", "50TB-100TB"),
    ("100TB-500TB", "100TB-500TB"),
    ("500TB-1PB", "500TB-1PB"),
    ("1PB-5PB", "1PB-5PB"),
    ("5PB-10PB", "5PB-10PB"),
    ("Above 10PB", "Above 10PB"),
]

COMPLETION_DATE_RANGES = [
    ("", "Select an option"),
    ("Less than 1 month", "Less than 1 month"),
    ("1-3 months", "1-3 months"),
    ("3-6 months", "3-6 months"),
    ("Above 12 months", "Above 12 months"),
]

ENVIRONMENT_ROLES = [
    (
        "developer",
        {
            "name": "Developer",
            "description": "Configures cloud-based IaaS and PaaS computing, networking, and storage services.",
        },
    ),
    (
        "database_administrator",
        {
            "name": "Database Administrator",
            "description": "Configures cloud-based database services.",
        },
    ),
    (
        "devops",
        {
            "name": "DevOps",
            "description": "Provisions, deprovisions, and deploys cloud-based IaaS and PaaS computing, networking, and storage services, including pre-configured machine images.",
        },
    ),
    (
        "billing_administrator",
        {
            "name": "Billing Administrator",
            "description": "Views cloud resource usage, budget reports, and invoices; Tracks budgets, including spend reports, cost planning and applicationions, and sets limits based on cloud service usage.",
        },
    ),
    (
        "security_administrator",
        {
            "name": "Security Administrator",
            "description": "Accesses information security and control tools of cloud resources which include viewing cloud resource usage logging, user roles and permissioning history.",
        },
    ),
    (
        "financial_auditor",
        {
            "name": "Financial Auditor",
            "description": "Views cloud resource usage and budget reports.",
        },
    ),
    (
        "",
        {"name": "No Access", "description": "User has no access to this environment."},
    ),
]

ENV_ROLE_MODAL_DESCRIPTION = {
    "header": "Assign Environment Role",
    "body": "An environment role determines the permissions a member of the portfolio assumes when using the JEDI Cloud.<br/><br/>A member may have different environment roles across different applications. A member can only have one assigned environment role in a given environment.",
}

FUNDING_TYPES = [
    ("", "- Select -"),
    ("RDTE", "Research, Development, Testing & Evaluation (RDT&E)"),
    ("OM", "Operations & Maintenance (O&M)"),
    ("PROC", "Procurement (PROC)"),
    ("OTHER", "Other"),
]

TASK_ORDER_SOURCES = [("MANUAL", "Manual"), ("EDA", "EDA")]

APP_MIGRATION = [
    ("on_premise", translate("forms.task_order.app_migration.on_premise")),
    ("cloud", translate("forms.task_order.app_migration.cloud")),
    ("both", translate("forms.task_order.app_migration.both")),
    ("none", translate("forms.task_order.app_migration.none")),
    ("not_sure", translate("forms.task_order.app_migration.not_sure")),
]

APPLICATION_COMPLEXITY = [
    ("storage", translate("forms.task_order.complexity.storage")),
    ("data_analytics", translate("forms.task_order.complexity.data_analytics")),
    ("conus", translate("forms.task_order.complexity.conus")),
    ("oconus", translate("forms.task_order.complexity.oconus")),
    ("tactical_edge", translate("forms.task_order.complexity.tactical_edge")),
    ("not_sure", translate("forms.task_order.complexity.not_sure")),
    ("other", translate("forms.task_order.complexity.other")),
]

DEV_TEAM = [
    ("civilians", translate("forms.task_order.dev_team.civilians")),
    ("military", translate("forms.task_order.dev_team.military")),
    ("contractor", translate("forms.task_order.dev_team.contractor")),
    ("other", translate("forms.task_order.dev_team.other")),
]

TEAM_EXPERIENCE = [
    ("none", translate("forms.task_order.team_experience.none")),
    ("planned", translate("forms.task_order.team_experience.planned")),
    ("built_1", translate("forms.task_order.team_experience.built_1")),
    ("built_3", translate("forms.task_order.team_experience.built_3")),
    ("built_many", translate("forms.task_order.team_experience.built_many")),
]

PERIOD_OF_PERFORMANCE_LENGTH = [
    (str(x + 1), translate_duration(x + 1)) for x in range(24)
]

REQUIRED_DISTRIBUTIONS = [
    ("contractor", "Contractor"),
    ("subcontractor", "Subcontractor"),
    ("cognizant_so", "Cognizant Security Office for Prime and Subcontractor"),
    ("overseas", "U.S. Activity Responsible for Overseas Security Administration"),
    ("administrative_ko", "Administrative Contracting Officer"),
    ("other", "Other as necessary"),
]

ENV_ROLES = [(role.value, role.value) for role in CSPRole] + [(None, "No access")]
