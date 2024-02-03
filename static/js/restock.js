
document.addEventListener('DOMContentLoaded', function () {
    var categorySelect = document.getElementById('id_Category');
    var contentTypeSelect = document.getElementById('id_content_type');
    var objectIdSelect = document.getElementById('id_object_id');
    var typeIdSelect = document.getElementById('id_Type');
    var branchField = document.getElementById('id_Branch');
    function updateDisplayAndOptions() {
        var category = categorySelect.value;

        // 根据category的值来隐藏或显示元素
        var displayStyle = category === '1' ? 'block' : 'none';
        contentTypeSelect.style.display = displayStyle;
        objectIdSelect.style.display = displayStyle;

        // 更新contentTypeSelect的选项
        if (category === '1') {
            contentTypeSelect.innerHTML = '<option value="7">分店</option>';
            typeIdSelect.innerHTML = '<option value="1">出貨</option>'
            const branchId = branchField.value;  // 获取当前选择的分店 ID
            console.log(branchId)
            fetch(`/Product/get-productss/${branchId}/`)  // 使用实际的 URL
            .then(response => response.json())
            .then(data => {
                const productSelect = document.getElementById('id_restockdetail_set-0-Product');
                const expiryDateField = document.getElementById('id_restockdetail_set-0-ExpiryDate');
                const numberField = document.getElementById('id_restockdetail_set-0-Number');
                productSelect.innerHTML = '';  // 清空现有选项
        
                data.forEach(item => {
                    const option = new Option(item.Product__Item_name + ' - ' + item.ExpiryDate, item.Product);
                    productSelect.appendChild(option);
                    option.setAttribute('data-id', item.id);
                });
                productSelect.addEventListener('change', function() {
                    const selectedOption = this.options[this.selectedIndex];
                    const itemId = selectedOption.getAttribute('data-id');
                    
                    // 然后使用这个 itemId 来查找数据
                    const selectedProduct = data.find(item => item.id === itemId);
                    if (selectedProduct) {
                        expiryDateField.value = selectedProduct.ExpiryDate;
                        numberField.value = selectedProduct.Remain;
                        numberField.setAttribute('max', selectedProduct.Remain);
                    }
                });
            })
            .catch(error => console.error('Error fetching products:', error));
        
        }else if(category === '0'){
            typeIdSelect.innerHTML = '<option value="0">進貨</option>'
            
        }
        else {
            contentTypeSelect.innerHTML = '<option value="7">分店7777777</option>'; // 所有选项的HTML
        }
    }

    categorySelect.addEventListener('change', updateDisplayAndOptions);
    updateDisplayAndOptions();  // 初始调用来设置初始状态
});

