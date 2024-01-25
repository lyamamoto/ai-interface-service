"""${message['revision']}"""

revision = '${message.revision}'
down_revision = '${message.down_revision}'
branch_labels = ${repr(message.branch_labels)}
depends_on = ${repr(message.depends_on)}

from alembic import op
import sqlalchemy as sa

${upgrades if upgrades else "# No changes in upgrade."}

${downgrades if downgrades else "# No changes in downgrade."}