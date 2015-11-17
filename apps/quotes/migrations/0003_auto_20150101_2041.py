from django.db import models, migrations

def remove_null_quote(apps, schema_editor):
    Quote = apps.get_model("quotes", "Quote")
    for i in Quote.objects.filter(comments=None):
        i.comments=''
        i.save()
        print "saved"
def remove_null_quoteline(apps, schema_editor):
    QuoteLineItem = apps.get_model("quotes", "QuoteLineItem")
    for j in QuoteLineItem.objects.filter(comments=None):
        j.comments=''
        j.save()
        print "saved"

class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_auto_20141231_0110'),
    ]

    operations = [
        migrations.RunPython(remove_null_quote),
        migrations.RunPython(remove_null_quoteline),
    ]