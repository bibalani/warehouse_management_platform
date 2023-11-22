<script type="text/javascript">
    $(document).ready(function(){
        $('#order_form').change(function(e){
            e.preventDefault();

            var serializedData = $(this).serialize();
            $.ajax({
                type: 'GET',
                url: "{% url 'my_app:get_form_info' %}",
                data: serializedData,
                success: function(response){
                    
                    
                    // var ser_current_inventory = JSON.parse(response['ser_current_inventory']);
                    // alert(ser_current_inventory)
                    
                    var current_inventory_fields = response['ser_current_inventory']['current_inventory'];
                    
                    

                    $('#maximum_quantity').val(current_inventory_fields)                                     
                },
                error: function(response){
                    console.log(response)
                }
            });            
        })
    });



$(document).ready(function(){
        $('#order_form').submit(function(e){
            e.preventDefault();

            var serializedData = $(this).serialize();
            $.ajax({
                type: 'POST',
                url: "{% url 'my_app:add_order_regular_customer' %}",
                data: serializedData,
                success: function(response){
                    $('#order_form').trigger('reset');

                    var ser_order = JSON.parse(response['ser_order']);
                    var fields = ser_order[0]['fields'];
                    $('#order_info tbody').DataTable.prepend(
                        `<tr>
                        <td>${fields["id"]||""}</td>
                        <td>${fields["sequence"]||""}</td>
                        <td>${fields["product"]||""}</td>
                        <td>${fields["quantity"]||""}</td>
                        <td>${fields["order_date"]||""}</td>
                        <td>${fields["source"]||""}</td>
                        <td>${fields["destination"]||""}</td>
                        </tr>`
                    )
                    location.reload();
                },
                error: function(response){
                    console.log(response)
                }
            });
            
        })
    });

    $(document).ready(function(){
    })

</script>


