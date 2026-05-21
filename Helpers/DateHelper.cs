namespace ImmiAccount.Helpers;

public static class DateHelper
{
    public static string Format(string? dateStr)
    {
        if (string.IsNullOrEmpty(dateStr)) return "";
        var s = dateStr.Length > 10 ? dateStr[..10] : dateStr;
        return DateTime.TryParse(s, out var dt) ? dt.ToString("d MMM yyyy") : dateStr;
    }
}
