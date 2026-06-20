# 🟨 Драйверы на C

> C — **главный язык драйверов**: на нём написаны ядра Linux/Windows и почти все драйверы. Разберём
> три сценария: модуль ядра Linux (char device), Windows (кратко), embedded (регистры).

> 🧭 Концепции — в [Интеграция · Драйверы](../Interop/04-drivers/21-kernel-module.md). Здесь — практика.
> ⚠️ Kernel-драйверы тестируй только в **виртуалке**.

---

## ⭐⭐ Linux: модуль ядра (char device)

### Минимальный модуль

```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>

static int __init mydrv_init(void) {
    printk(KERN_INFO "mydrv: загружен\n");   // printk — «printf ядра», вывод в dmesg
    return 0;                                 // 0 = успех
}
static void __exit mydrv_exit(void) {
    printk(KERN_INFO "mydrv: выгружен\n");
}

module_init(mydrv_init);                      // что вызвать при insmod
module_exit(mydrv_exit);                      // что вызвать при rmmod
MODULE_LICENSE("GPL");                         // обязательно (иначе ядро «tainted»)
MODULE_AUTHOR("Ты");
MODULE_DESCRIPTION("Учебный драйвер");
```

```makefile
# Makefile — сборка против заголовков текущего ядра
obj-m += mydrv.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

```bash
make
sudo insmod mydrv.ko      # загрузить
dmesg | tail              # увидеть "mydrv: загружен"
sudo rmmod mydrv          # выгрузить
```

💡 ⭐⭐ Скелет модуля ядра: **init/exit + module_init/module_exit + MODULE_LICENSE**. Сборка — через
Makefile ядра (`obj-m`), управление — `insmod`/`rmmod`, вывод — `printk` → `dmesg`. В ядре **нет
libc**: ни `printf`, ни `malloc` — только ядровые API (`printk`, `kmalloc`, `copy_to_user`).

---

### Char device — общение с userspace через /dev

```c
#include <linux/fs.h>
#include <linux/uaccess.h>     // copy_to_user / copy_from_user
#include <linux/cdev.h>

static char buffer[256];
static int major;

// чтение из /dev/mydev → вызывается, когда userspace делает read()
static ssize_t mydrv_read(struct file *f, char __user *buf, size_t len, loff_t *off) {
    size_t n = min(len, sizeof(buffer));
    if (copy_to_user(buf, buffer, n))     // ⚠️ нельзя просто memcpy в user-указатель!
        return -EFAULT;
    return n;
}
static ssize_t mydrv_write(struct file *f, const char __user *buf, size_t len, loff_t *off) {
    size_t n = min(len, sizeof(buffer));
    if (copy_from_user(buffer, buf, n))
        return -EFAULT;
    return n;
}

static struct file_operations fops = {       // таблица: какие функции на какие операции
    .owner = THIS_MODULE,
    .read  = mydrv_read,
    .write = mydrv_write,
};

// в init: major = register_chrdev(0, "mydev", &fops);
// затем создать /dev/mydev (mknod или udev)
```

```bash
echo "привет" | sudo tee /dev/mydev   # вызовет mydrv_write
sudo cat /dev/mydev                    # вызовет mydrv_read
```

💡 ⭐⭐ Char device связывает железо/драйвер с приложениями через файл `/dev/...`: userspace делает
`read`/`write`/`ioctl` → ядро зовёт твои функции из `file_operations`. **Главное правило безопасности:
данные между ядром и userspace — только через `copy_to_user`/`copy_from_user`** (нельзя разыменовывать
user-указатель напрямую — это дыра/краш). `ioctl` — для команд устройству (см. трек Интеграция).

---

## ⭐ Доступ к железу из драйвера

```c
   // память-mapped регистры устройства (MMIO):
   void __iomem *regs = ioremap(phys_addr, size);   // отобразить физ. адрес
   u32 status = ioread32(regs + STATUS_REG);         // читать регистр
   iowrite32(value, regs + CONTROL_REG);             // писать регистр
   iounmap(regs);

   // прерывания: request_irq(irq, handler, ...) — обработчик при сигнале от железа.
   // DMA, kmalloc(GFP_KERNEL), спинлоки/мьютексы для синхронизации — арсенал ядра.
```

💡 ⭐ Драйвер «дёргает железо» через MMIO (`ioread/iowrite` по отображённым регистрам) и реагирует на
**прерывания** (`request_irq`). Это и есть «разговор с устройством». Конкретные регистры/протокол —
из даташита железа.

---

## 📖 Windows (кратко) и userspace

```
   WINDOWS (ядро): язык — C (иногда ограниченный C++). фреймворки WDM (старый) / KMDF (современный, проще).
   • точка входа DriverEntry(), сборка через WDK (Windows Driver Kit) в Visual Studio.
   • ⚠️ ядровый драйвер ОБЯЗАН быть ПОДПИСАН (и Secure Boot) — иначе не загрузится.
   • userspace-аналог: UMDF (драйвер в user-mode, безопаснее).

   USERSPACE на Linux (без написания модуля ядра — проще и безопаснее):
   • libusb — говорить с USB-устройством из обычной C-программы.
   • UIO / VFIO — отдать PCI-устройство в userspace.
   • FUSE — своя файловая система в userspace.
```

💡 Если можно — делай **userspace-драйвер** (libusb/UIO): упал — упал процесс, а не система; проще
отлаживать обычным gdb. Kernel-драйвер пиши, только когда нужен (производительность, ранний этап
загрузки, нет userspace-интерфейса).

---

## ⚙️ Embedded на C (без ОС)

```c
   // прямой доступ к регистру микроконтроллера (пример «мигни светодиодом», STM32-стиль):
   #define GPIOA_BASE  0x40020000u
   #define GPIOA_ODR   (*(volatile uint32_t*)(GPIOA_BASE + 0x14))  // регистр выходных данных

   GPIOA_ODR |=  (1 << 5);   // зажечь пин 5
   GPIOA_ODR &= ~(1 << 5);   // погасить
   // volatile — ОБЯЗАТЕЛЬНО: говорит компилятору «не оптимизируй, это железо».
```

💡 ⭐ В embedded «драйвер» = код доступа к периферии: пишешь в регистры по адресам из даташита.
**`volatile` обязательно** (иначе компилятор «соптимизирует» обращения к железу). Вендоры дают HAL
(STM32 HAL, CMSIS) — обёртки над регистрами. Связь с [битовыми операциями](../C/03-middle/18-bitwise.md)
(маски/сдвиги для битов в регистрах).

---

## ⚠️ Ловушки (C-драйверы)

- ❌ Разыменовать user-указатель напрямую в ядре (нужен `copy_to/from_user`) → краш/дыра.
- ❌ Тестировать kernel-драйвер на рабочей ОС (баг = kernel panic) → используй ВМ.
- ❌ Забыть `volatile` для MMIO/регистров (компилятор уберёт «лишние» обращения).
- ❌ Забыть `MODULE_LICENSE("GPL")` / освободить ресурсы в exit (утечки в ядре опасны).
- ❌ Долгие операции/сон в обработчике прерывания (нельзя блокироваться) — отложенная работа.
- ❌ На Windows — неподписанный ядровый драйвер не загрузится.

---

## ✅ Задачи

1. Собери минимальный модуль ядра в Linux-ВМ: insmod → `dmesg` → rmmod. Увидь свои сообщения.
2. Добавь char device (`file_operations` + read/write через `copy_to/from_user`). Проверь через `cat`/`echo`.
3. ⭐ Embedded: на плате (или эмуляторе) помигай светодиодом через прямой доступ к регистру GPIO.
4. ⭐ Userspace: через libusb прочитай дескриптор подключённого USB-устройства (без модуля ядра).
5. Объясни, почему в ядре нельзя `printf`/`malloc` и чем их заменяют.

---

## ❓ Проверь себя

1. Из чего состоит минимальный модуль ядра Linux?
2. Как драйвер общается с userspace (char device, `file_operations`, copy_to/from_user)?
3. Как драйвер обращается к железу (MMIO, прерывания)?
4. Почему `volatile` обязателен для регистров?
5. Когда выбрать userspace-драйвер вместо kernel?

➡️ Сравни: [🟦 C++](DRIVERS-CPP.md) · [🦀 Rust](DRIVERS-RUST.md) · [обзор](README.md)
