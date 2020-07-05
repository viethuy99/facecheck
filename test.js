var a = "'a', 'a', 'a', 'a', 'a', 'A', 'a', 'a', 'a', 'a', 'a', 'a', 'A', 'A', 'A', 'A', 'A', 'A', 'a', 'a', 'a', 'a', 'a', 'a', 'A', 'A', 'A', 'A', 'A', 'A', 'a', 'a', 'a', 'a', 'a', 'a', 'E', 'E', 'E', 'E', 'E', 'E', 'e', 'e', 'e', 'e', 'e', 'e', 'E', 'E', 'E', 'E', 'E', 'E', 'e', 'e', 'e', 'e', 'e', 'e', 'I', 'I', 'I', 'I', 'I', 'I', 'i', 'i', 'i', 'i', 'i', 'i', 'U', 'U', 'U', 'U', 'U', 'U', 'u', 'u', 'u', 'u', 'u', 'u', 'U', 'U', 'U', 'U', 'U', 'U', 'u', 'u', 'u', 'u', 'u', 'u', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'y', 'y', 'y', 'y', 'y', 'y', 'O', 'O', 'O', 'O', 'O', 'O', 'o', 'o', 'o', 'o', 'o', 'o', 'O', 'O', 'O', 'O', 'O', 'O', 'o', 'o', 'o', 'o', 'o', 'o', 'O', 'O', 'O', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'd', 'd')"
var b = ""
b = ""
// z = int('A') - int('a')
// console.log(z)
for (var i = 0; i < a.length; i++) {
    if (a[i] >= 'A' && a[i] <= 'Z') {
        b += String.fromCharCode(a.charCodeAt(i) + 32)
    }
        
    else  b += a[i]
}
    
console.log(b)