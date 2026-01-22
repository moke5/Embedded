[hello算法](https://www.hello-algo.com/)

## 查找



### 二分查找

```c
int binarySearch(int *arr, int size, int target)
{
    int left = arr[0], right = arr[size - 1];
    while (left <= right)
    {
        // 使用(right + left)可能会越界
        int mid = left + (right - left) / 2;

        if (arr[mid] == target)
        {
            return mid;
        }
        else if (arr[mid] < target)
        {
            left = mid + 1;
        }
        else
        {
            right = mid - 1;
        }
    }
    return -1;
}
```



## 排序



### 选择排序



```c
int selectSort(int *arr, int n)
{
    for (size_t i = 0; i < n - 1; i++)
    {
        int minIdex = i;
        for (size_t j = i + 1; j < n; j++)
        {
            if (arr[j] < arr[minIdex])
            {
                minIdex = j;
            }
        }
        int temp = arr[i];
        arr[i] = arr[minIdex];
        arr[minIdex] = temp;
    }
}
```



### 插入排序



```c
void insertionSort(int *arr, int size)
{
    for (size_t i = 1; i < size; i++)
    {
        int base = arr[i], j = i - 1;
        while (j >= 0 && arr[j] > base)
        {
            arr[j + 1] = arr[j];
            j--;
        }
       arr[j + 1] = base;
    }
}
```



### 快速排序



```c
void swap(int *i, int *j)
{
    int temp = *i;
    *i = *j;
    *j = temp;
}

int partition(int *arr, int left, int right)
{
    int i = left, j = right;
    while (i < j)
    {
        while (arr[j] >= arr[left] && i < j)
        {
            j--;
        }
        while (arr[i] <= arr[left] && i < j)
        {
            i++;
        }
        swap(arr + i, arr + j);
    }
    swap(arr + left, arr + i);
    return i;
}

void quickSort(int *arr, int left, int right)
{
    if (left >= right)
    {
        return;
    }
    int i = partition(arr, left, right);
    quickSort(arr, left, i - 1);
    quickSort(arr, i + 1, right);
}
```



