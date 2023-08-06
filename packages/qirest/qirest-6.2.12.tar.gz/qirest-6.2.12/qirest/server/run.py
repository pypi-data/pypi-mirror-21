#!/usr/bin/env python
import importlib
import mongoengine
from eve import Eve
from eve_mongoengine import EveMongoengine
from qirest_client.model.subject import (Project, ImagingCollection, Subject)
from qirest_client.model.imaging import (SessionDetail, Scan, Protocol)

# The application.
app = Eve()

# The MongoEngine ORM extension.
ext = EveMongoengine(app)

# Register the model non-embedded documdent classes.
ext.add_model(Project, url='project')
ext.add_model(ImagingCollection, url='imaging-collection')
ext.add_model(Subject, url='subject')
ext.add_model(SessionDetail, url='session-detail')
ext.add_model(Protocol, url='protocol')


if __name__ == '__main__':
    app.run()
