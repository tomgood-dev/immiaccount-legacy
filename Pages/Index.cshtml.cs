using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace ImmiAccount.Pages;

public class IndexModel : PageModel
{
    public IActionResult OnGet()
    {
        if (HttpContext.Session.GetInt32("UserId") != null)
            return RedirectToPage("/Applications/Index");
        return RedirectToPage("/Login");
    }
}
