document.addEventListener('DOMContentLoaded', function() {
    const noticeTypeField = document.getElementById('id_notice_type');
    const pdfFieldset = document.querySelector('.field-pdf_file').closest('fieldset');
    const textFieldsets = document.querySelectorAll('.field-summary, .field-content');
    
    function toggleFields() {
        const noticeType = noticeTypeField.value;
        
        if (noticeType === 'pdf') {
            // Show PDF field, hide text fields
            if (pdfFieldset) pdfFieldset.style.display = 'block';
            textFieldsets.forEach(fieldset => {
                if (fieldset.closest('fieldset')) {
                    fieldset.closest('fieldset').style.display = 'none';
                }
            });
        } else if (noticeType === 'text') {
            // Show text fields, hide PDF field
            if (pdfFieldset) pdfFieldset.style.display = 'none';
            textFieldsets.forEach(fieldset => {
                if (fieldset.closest('fieldset')) {
                    fieldset.closest('fieldset').style.display = 'block';
                }
            });
        }
    }
    
    // Initial toggle
    if (noticeTypeField) {
        toggleFields();
        noticeTypeField.addEventListener('change', toggleFields);
    }
});
