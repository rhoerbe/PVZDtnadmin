from datetime import timedelta

from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import site
from django.utils import timezone
from django.conf import settings
from ..models.constants import *
from ..signals import md_statement_edit_starts
from ..models import CheckOut, MDstatement
from PVZDpy.cresignedxml import creSignedXML
from PVZDpy.samlentitydescriptor import SAMLEntityDescriptorFromStrFactory, SAMLEntityDescriptor


class MDstatementForm(forms.ModelForm):

    class Meta:
        model = MDstatement
        exclude = ['checkout_status']

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.ed_uploaded:
            if not cleaned_data.get("ed_file_upload"):
                self.add_error('ed_file_upload', 'Es wurde noch kein EntityDescriptor hochgeladen')


site.disable_action('delete_selected')


@admin.register(MDstatement)
class MDstatementAdmin(admin.ModelAdmin):
    form = MDstatementForm
    actions = ['sign_ed']
    save_on_top = True
    readonly_fields = (
        'authorized',
        'created_at',
        'ed_signed',
        'ed_uploaded',
        'ed_uploaded_filename',
        'entityID',
        'get_boilerplate_help',
        'get_signer_subject',
        'get_validation_message',
        'is_delete',
        'namespace',
        'orgcn',
        'orgid',
        'status',
        'updated_at',
        'valid',
    )
    list_display = (
        'entityID',
        'status',
        'valid',
        'authorized',
        'is_delete',
        'namespace',
        'orgid',
        'get_signer_subject',
        'get_validation_message_trunc',
        'updated',
        'admin_note',
    )
    search_fields = ('entityID', 'status', )
    fieldsets = (
        (None, {
            'fields': ('get_boilerplate_help', )
        }),
        ('Entity', {
            'fields': (
                'entityID',
                'is_delete',
            )
        }),
        ('Datei hochladen', {
            'fields': (
                'ed_file_upload',
                'ed_uploaded_filename',
            )
        }),
        ('Prozess Status', {
            'fields': (
                'status',
                'valid',
                'authorized',
                'get_validation_message',
            )
        }),
        ('Adminsitrative Attribute', {
            'fields': (
                ('created_at', 'updated_at', ),
                'get_signer_subject',
                'admin_note',
            )
        }),
        ('EntityDescriptor XML', {
            'classes': ('collapse',),
            'fields': ('ed_uploaded', 'ed_signed', ),
        }),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        delta_min = getattr(settings, 'PORTALADMIN_CHECKOUT_MINUTES', 15)
        datetime_ago = timezone.now() - timedelta(minutes=delta_min)

        try:
            md_statement = MDstatement.objects.get(id=object_id)
        except MDstatement.DoesNotExist:
            return

        if md_statement.checkout_status:
            # CheckOut by another user
            if md_statement.checkout_status.checkout_by != request.user \
                    and md_statement.checkout_status.created_at > datetime_ago:
                # we need to create custom error page or disable UI of admin form
                assert False, 'The Metadata Statement is locked by another user, please try again later'

        md_statement_edit_starts.send(sender=MDstatement, md_statement=md_statement, current_user=request.user)

        return super().change_view(request, object_id, form_url, extra_context)

    def sign_ed(modeladmin, request, queryset):
        if len(queryset.all()) > 1:
            messages.error(request, "Bitte genau einen EntityDescriptor auswählen")
        this_rec = queryset.all()[0]
        ed_pk = this_rec.pk
        ed = SAMLEntityDescriptorFromStrFactory(this_rec.ed_uploaded)
        ed.remove_enveloped_signature()
        md_namespace_prefix = ed.get_namespace_prefix()
        try:
            signed_contents = creSignedXML(ed.get_xml_str(),
                                           sig_type='enveloped',
                                           sig_position='/' + md_namespace_prefix + ':EntityDescriptor')
            MDstatement.objects.filter(pk=ed_pk).update(ed_signed=signed_contents,
                                                        status=STATUS_REQUEST_QUEUE)
            messages.info(request, "EntityDescriptor signiert und Status auf 'submitted' gesetzt")
        except(Exception) as e:
            messages.error(request, "Fehler bei der Signaturanforderung: " + str(e))
        pass
    sign_ed.short_description = "EntityDescriptor mit lokaler BKU signieren"

    def get_action_choices(self, request):
        # remove default blank selection in action drop-down
        choices = super(MDstatementAdmin, self).get_action_choices(request)
        choices.pop(0) # choices is a list, the first is the BLANK_CHOICE_DASH
        return choices
