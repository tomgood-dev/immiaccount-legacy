using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace ImmiAccount.Pages;

public abstract class PageModelBase : PageModel
{
    private const string KeyUserId = "UserId";
    private const string KeyDisplayName = "DisplayName";
    private const string KeyLastActivity = "LastActivity";
    private const int TimeoutMinutes = 20;

    protected int? CurrentUserId => HttpContext.Session.GetInt32(KeyUserId);

    protected IActionResult? CheckAuth()
    {
        if (HttpContext.Session.GetInt32(KeyUserId) == null)
            return RedirectToPage("/Login");

        var lastStr = HttpContext.Session.GetString(KeyLastActivity);
        if (lastStr != null && DateTime.TryParse(lastStr, out var last))
        {
            if (DateTime.UtcNow - last > TimeSpan.FromMinutes(TimeoutMinutes))
            {
                HttpContext.Session.Clear();
                TempData["TimeoutMessage"] = "Your session has timed out due to inactivity. Please log in again.";
                return RedirectToPage("/Login");
            }
        }

        HttpContext.Session.SetString(KeyLastActivity, DateTime.UtcNow.ToString("O"));
        return null;
    }
}
