document.addEventListener("DOMContentLoaded", function () {
var leftList = document.getElementById("left-list");
var rightSlots = document.querySelectorAll(".sortable-slot");
var submitBtn = document.getElementById("submit-btn");

const FieldName = js_vars.field_name;
var hiddenInput = document.getElementById(FieldName);

console.log('field name',FieldName);



// Initialize sortable for left list (unranked items)
new Sortable(leftList, {
    group: "shared",
    animation: 150,
});

// Initialize sortable for each ranking slot (only one item per slot)
rightSlots.forEach(slot => {
    new Sortable(slot, {
        group: "shared",
        animation: 150,
        swapThreshold: 1,
        onAdd: function (evt) {
            let item = evt.item;
            
            // Remove placeholder when an item is added
            let placeholder = slot.querySelector(".placeholder");
            if (placeholder) {
                placeholder.remove();
            }

            // Move previous item back to left list if slot already had an item
            if (slot.children.length > 1) {
                leftList.appendChild(slot.children[0]);  // Move first item back (originally in slot)
            }

            updateRankingOrder();
        },
        onRemove: function (evt) {
            // Restore placeholder if slot becomes empty
            if (slot.children.length === 0) {
                let placeholderSpan = document.createElement("span");
                placeholderSpan.classList.add("placeholder");
                placeholderSpan.textContent = "[Drag&Drop here]";
                slot.appendChild(placeholderSpan);
            }
            updateRankingOrder();
        }
    });
});

function updateRankingOrder() {
    var order = [];
    rightSlots.forEach(slot => {
        let item = slot.querySelector(".sortable-item");
        order.push(item ? item.dataset.value : null);
    });

    hiddenInput.value = JSON.stringify(order);

    // Enable submit button only if all slots are filled
    submitBtn.disabled = order.includes(null);
}

submitBtn.addEventListener("click", function () {
    updateRankingOrder();
    document.forms[0].submit();
});
});