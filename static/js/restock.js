document.addEventListener('DOMContentLoaded', function () {
    var categorySelect = document.getElementById('id_Category');
    var contentTypeSelect = document.getElementById('id_content_type');
    var objectIdSelect = document.getElementById('id_object_id');
    var typeIdSelect = document.getElementById('id_Type');

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

// document.addEventListener('DOMContentLoaded', function () {
//     var categorySelect = document.getElementById('id_Category');
//     var objectIdSelect = document.getElementById('id_object_id');

//     function updateObjectIdOptions() {
//         var category = categorySelect.value;
//         // 清空 objectIdSelect 的当前选项
//         objectIdSelect.innerHTML = '';

//         if (category === '1') { // 假设 1 代表 'BtoB'
//             // 使用 AJAX 获取 Branchs 的数据
//             fetch('/Product/get_branches/') // 请替换为实际的 API URL
//                 .then(response => response.json())
//                 .then(data => {
//                     data.forEach(branch => {
//                         var option = document.createElement('option');
//                         option.value = branch.id;  // 确保这是一个整数
//                         option.textContent = branch.Name;
//                         objectIdSelect.appendChild(option);
//                     });
                    
//                 });
//         }
//     }

//     categorySelect.addEventListener('change', updateObjectIdOptions);

//     // 初始调用
//     updateObjectIdOptions();
// });
