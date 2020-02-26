
  $(function () {
    // fs create
      $('.js-create-fs').click(function () {
        var parent = $(this).parent()
        console.log(parent)
        var ul = parent.find('.list-unstyled')
        var id = ul.attr("id");
        var idno = id.slice(2)
        url = '/order/' + idno + '/fittingsample/'
        console.log(url)
        $.ajax({
          url: url,
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-fs").modal("show");
          },
          success: function (data) {
            $("#modal-fs .modal-content").html(data.html_form);
          }
        });
      });
      // fs save
      $("#modal-fs").on("submit", ".js-fs-create-form", function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function (data) {
            pk = data['pk']
            id = 'fs' + pk
            element = $('#' + id);
            if (data.form_is_valid) {
              element.html(data.html_fs_list);  // <-- Replace the table body
              $("#modal-fs").modal("hide");  // <-- Close the modal
            }
            else {
              $("#modal-fs .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      });
      // fs delete
      $(document).on('click', '.fs-delete', function () {
        var id = $(this).attr("id");
        var idno = id.slice(3)
        url = '/order/' + 'fs/' + idno + '/delete/'
        console.log(url)
        $.ajax({
          url: url,
          type: 'get',
          dataType: 'json',
          success: function (data) {
            pk = data['pk']
            id = 'fs' + pk
            element = $('#' + id);
            if (data.form_is_valid) {
              element.html(data.html_fs_list);  // <-- Replace the table body
              $("#modal-fs").modal("hide");  // <-- Close the modal
            }
          }
        });
      });
      // fs edit
      $(document).on('click', '.fs-edit', function () {
        var id = $(this).attr("id");
        var idno = id.slice(3)
        url = '/order/' + 'fs/' + idno + '/edit/'
        console.log(url)
        $.ajax({
          url: url,
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-fs").modal("show");
          },
          success: function (data) {
            pk = data['pk']
            id = 'fs' + pk
            element = $('#' + id);
            if (data.form_is_valid) {
              element.html(data.html_fs_list);  // <-- Replace the table body
              $("#modal-fs").modal("hide");  // <-- Close the modal
            }
            else {
              $("#modal-fs .modal-content").html(data.html_form);
            }
          }
        });
      });

    });
