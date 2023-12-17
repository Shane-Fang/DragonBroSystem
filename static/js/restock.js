document.addEventListener('DOMContentLoaded', function () {
    function toggleFields() {
        var category = document.getElementById('id_Category').value;
        var displayStyle = category == '1' ? 'block' : 'none';
        document.getElementById('id_content_type').style.display = displayStyle;
        document.getElementById('id_object_id').style.display = displayStyle;
    }
    document.getElementById('id_Category').addEventListener('change', toggleFields);
    toggleFields();

});
document.addEventListener('DOMContentLoaded', function () {
    var categorySelect = document.getElementById('id_Category');
    var contentTypeSelect = document.getElementById('id_content_type');
    var objectIdSelect = document.getElementById('id_object_id');

    function updateContentTypeOptions() {
        var category = categorySelect.value;

        if (category === '1') {  // 假設 1 代表 'BtoB'
            contentTypeSelect.innerHTML = '<option value="7">分店</option>';
            
        } else {
            contentTypeSelect.innerHTML = '...'; // 所有選項的 HTML
        
        }
    }
    categorySelect.addEventListener('change', updateContentTypeOptions);


    updateContentTypeOptions(); // 初始呼叫
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
