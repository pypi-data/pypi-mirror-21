/* global Handlebars componentHandler url_api_v1_device_delete
   url_api_v1_device_show_user
   username */
/* exported deleteDevice */

/* Global list state */
var devices_list;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-devices').html();

$(document).ready(function(){
  /* Start templating */
  get_devices();
});

/* Call APIs to get the JSON devices-list */
function get_devices() {
  /* Get the list of stages */
  devices_list = {devices: []};
  $.getJSON(url_api_v1_device_show_user.replace('0', username), function(devices){
    for (var i = 0, len = devices.length; i < len; i++) {
      devices_list.devices.push({
        name: devices[i].fields.name,
        MAC: devices[i].pk
      });
    }
    renderTemplate(devices_list);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 404) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

/* render compiled handlebars template */
function renderTemplate(devices_list){
  var template = Handlebars.compile(source);
  $('#listCard').html(template(devices_list));
  /* Make MDL re-register progress-bars and the like */
  componentHandler.upgradeDom();
}

/* delete a device */
function deleteDevice(MAC) {
  $.get(url_api_v1_device_delete.replace('00:00:00:00:00:00', MAC), function(){
    var device_index = devices_list.devices.findIndex(function(element){
      return element.MAC == MAC;
    });
    devices_list.devices.splice(device_index, 1);
    renderTemplate(devices_list);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

$('#newDeviceForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  var form_data = $('#newDeviceForm');
  $.post(event.target.action, form_data.serialize(), function() {
    var new_device = form_data.serializeArray().reduce(function(obj, item) {
      obj[item.name] = item.value;
      return obj;
    }, {});
    var device = {};
    device.name = new_device['name'];
    device.MAC =  new_device['MAC'];
    devices_list.devices.push(device);
    renderTemplate(devices_list);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 400 || jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    })
    .always(function() {
      form_data.trigger('reset');
    });
}
